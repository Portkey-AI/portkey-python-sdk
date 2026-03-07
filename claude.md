# Portkey Python SDK - Architecture Guide

## Overview

Portkey is an AI Gateway that unifies LLM signatures. This SDK wraps the OpenAI Python SDK using a **vendoring approach** to avoid conflicts with user-installed OpenAI packages.

## Directory Structure

```
portkey-python-sdk/
├── portkey_ai/
│   ├── __init__.py              # Public API - exports all classes
│   ├── version.py               # SDK version
│   ├── _vendor/                 # Vendored dependencies
│   │   └── openai/              # Vendored OpenAI SDK (currently v2.16.0)
│   ├── api_resources/           # Core SDK implementation
│   │   ├── __init__.py          # Internal exports
│   │   ├── client.py            # Portkey & AsyncPortkey clients
│   │   ├── base_client.py       # APIClient & AsyncAPIClient base classes
│   │   ├── apis/                # API endpoint implementations
│   │   │   ├── api_resource.py  # Base class for all resources
│   │   │   ├── chat_complete.py # OpenAI wrapper example
│   │   │   ├── containers.py    # OpenAI wrapper example
│   │   │   ├── feedback.py      # Portkey-specific endpoint
│   │   │   └── ...
│   │   └── types/               # Response type definitions
│   │       ├── chat_complete_type.py
│   │       ├── containers_type.py
│   │       └── ...
│   ├── integrations/            # Third-party integrations (ADK, Strands)
│   ├── langchain/               # LangChain integration
│   └── llamaindex/              # LlamaIndex integration
├── vendorize.toml               # Vendoring configuration
└── tests/                       # Test suite
```

## Vendoring Approach

The SDK vendors the OpenAI Python SDK to avoid version conflicts:

```toml
# vendorize.toml
target = "portkey_ai/_vendor"
packages = ["openai==2.16.0"]  # Update this version as needed
```

### Key Vendoring Quirks

#### 1. Import Paths
Two styles are used (both are valid):
```python
# Absolute import (preferred for types used in type hints)
from portkey_ai._vendor.openai import OpenAI, AsyncOpenAI
from portkey_ai._vendor.openai._types import Omit, omit

# Relative import (used within api_resources/)
from ..._vendor.openai._types import Omit, omit, FileTypes
```

#### 2. Placeholder API Key
The vendored OpenAI client requires an API key, but Portkey uses headers for auth:
```python
# global_constants.py
OPEN_AI_API_KEY = "OPENAI_API_KEY"  # Just a placeholder string!

# client.py
self.openai_client = OpenAI(
    api_key=OPEN_AI_API_KEY,  # Satisfies OpenAI client requirement
    base_url=self.base_url,   # Points to Portkey gateway
    default_headers=self.allHeaders,  # Actual auth via x-portkey-api-key header
)
```

#### 3. Linting Exclusions
The vendored code is excluded from all linters/formatters:
```toml
# pyproject.toml
[tool.mypy]
exclude = ['portkey_ai/_vendor', 'tests']

[[tool.mypy.overrides]]
module = 'portkey_ai._vendor.*'
ignore_errors = true

[tool.black]
force-exclude = '''(portkey_ai/_vendor)/'''

[tool.ruff]
exclude = ["portkey_ai/_vendor", "tests"]
```

#### 4. Type Reuse vs Redefinition
**Response types** - OpenAI types are imported directly for nested types:
```python
# types/response_type.py
from portkey_ai._vendor.openai.types.responses.response import ToolChoice
from portkey_ai._vendor.openai.types.responses.response_output_item import ResponseOutputItem

class Response(BaseModel, extra="allow"):
    tool_choice: ToolChoice  # Direct reuse of OpenAI type
    output: List[ResponseOutputItem]  # Direct reuse
    # ... but top-level response adds _headers support
    _headers: Optional[httpx.Headers] = PrivateAttr()
```

**Param types** - OpenAI param types are imported directly in API wrappers:
```python
# apis/containers.py
from portkey_ai._vendor.openai.types import container_create_params

def create(
    self,
    expires_after: Union[container_create_params.ExpiresAfter, Omit] = omit,
):
    ...
```

While **top-level response types** are redefined in Portkey to add header support:
```python
# Portkey redefines simple types to add _headers
class ContainerCreateResponse(BaseModel, extra="allow"):
    id: Optional[str] = None
    # ... mirrors OpenAI type but adds:
    _headers: Optional[httpx.Headers] = PrivateAttr()
```

#### 5. _vendor/__init__.py is Empty
The `_vendor/__init__.py` file is empty - imports go directly to `_vendor/openai/`

#### 6. Custom Streaming Implementation
Portkey has its **own SSE streaming implementation** in `streaming.py` for Portkey-specific endpoints, separate from OpenAI's streaming (used for OpenAI wrapper endpoints)

## Client Architecture

### Main Clients (`client.py`)

```python
class Portkey(APIClient):
    def __init__(self, *, api_key, base_url, virtual_key, config, ...):
        # Initialize base client with headers
        super().__init__(...)
        
        # Create vendored OpenAI client pointing to Portkey gateway
        self.openai_client = OpenAI(
            api_key=OPEN_AI_API_KEY,  # Placeholder key
            base_url=self.base_url,   # Portkey gateway URL
            default_headers=self.allHeaders,
        )
        
        # Initialize all API resources
        self.completions = apis.Completion(self)
        self.chat = apis.ChatCompletion(self)
        self.containers = apis.Containers(self)
        # ... more resources
```

### Two Types of API Endpoints

#### 1. OpenAI Wrapper Endpoints

These wrap the vendored OpenAI client and proxy requests through Portkey:

```python
# Example: containers.py
class Containers(APIResource):
    def __init__(self, client: Portkey):
        super().__init__(client)
        self.openai_client = client.openai_client

    def create(self, *, name: str, expires_after: Union[ExpiresAfter, Omit] = omit, ...):
        # Use with_raw_response to access headers
        response = self.openai_client.with_raw_response.containers.create(
            name=name,
            expires_after=expires_after,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        # Parse response and attach headers
        data = ContainerCreateResponse(**json.loads(response.text))
        data._headers = response.headers
        return data
```

#### 2. Portkey-Specific Endpoints

These use the internal HTTP client directly:

```python
# Example: feedback.py
class Feedback(APIResource):
    def create(self, *, trace_id, value, weight, metadata):
        body = dict(trace_id=trace_id, value=value, weight=weight, metadata=metadata)
        return self._post(
            PortkeyApiPaths.FEEDBACK_API,
            body=body,
            params=None,
            cast_to=FeedbackResponse,
            stream_cls=Stream[FeedbackResponse],
            stream=False,
            headers={},
        )
```

## Key Patterns

### 1. Union Types with `Omit` vs `NotGiven`

**Important distinction** - These are NOT interchangeable:

| Sentinel | Use Case | Behavior |
|----------|----------|----------|
| `Omit` / `omit` | Parameter should not be sent in request | Omits key from JSON body |
| `NotGiven` / `NOT_GIVEN` | Parameter has meaningful `None` value | Distinguishes "not provided" from "explicitly None" |

```python
from portkey_ai._vendor.openai._types import Omit, omit, NOT_GIVEN, NotGiven

def create(
    self,
    *,
    # Use Omit for params that should be omitted when not provided
    expires_after: Union[ExpiresAfter, Omit] = omit,
    file_ids: Union[List[str], Omit] = omit,
    
    # Use NotGiven for params where None is a valid, distinct value
    # e.g., timeout=None means "no timeout", timeout=NOT_GIVEN means "use default"
    timeout: Union[float, httpx.Timeout, None, NotGiven] = NOT_GIVEN,
):
    ...
```

**Pattern used in codebase:**
- OpenAI wrapper endpoints: Prefer `Omit`/`omit` for most optional params
- `timeout` parameter: Always uses `NotGiven`/`NOT_GIVEN`
- The codebase uses both `NOT_GIVEN` (constant) and `not_given` (instance) - they're aliases

### 2. Response Headers Handling

All response types include a private `_headers` attribute:

```python
# types/containers_type.py
class ContainerCreateResponse(BaseModel, extra="allow"):
    id: Optional[str] = None
    name: Optional[str] = None
    # ... other fields
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)
```

Set headers after parsing response:
```python
response = self.openai_client.with_raw_response.containers.create(...)
data = ContainerCreateResponse(**json.loads(response.text))
data._headers = response.headers
return data
```

### 3. Extra Parameters via `**kwargs`

Extract OpenAI's extra parameters from kwargs:

```python
def create(self, *, name: str, **kwargs):
    extra_headers = kwargs.pop("extra_headers", None)
    extra_query = kwargs.pop("extra_query", None)
    extra_body = kwargs.pop("extra_body", None)
    timeout = kwargs.pop("timeout", None)
    
    # Merge remaining kwargs into extra_body
    user_extra_body = extra_body or {}
    merged_extra_body = {**user_extra_body, **kwargs}
```

### 4. Streaming vs Non-Streaming

For endpoints that support streaming:

```python
def create(self, *, stream: Union[bool, Omit] = omit, **kwargs):
    if stream is True:
        # Return iterator directly (no raw response needed)
        return self.openai_client.chat.completions.create(stream=True, ...)
    else:
        # Use with_raw_response for headers
        response = self.openai_client.with_raw_response.chat.completions.create(...)
        data = ChatCompletions(**json.loads(response.text))
        data._headers = response.headers
        return data
```

### 5. Sync/Async Pairs

Every resource has both sync and async versions:

```python
class Containers(APIResource):
    def create(self, ...) -> ContainerCreateResponse:
        ...

class AsyncContainers(AsyncAPIResource):
    async def create(self, ...) -> ContainerCreateResponse:
        ...
```

## Type Definitions

Types are defined in `portkey_ai/api_resources/types/`:

```python
# types/containers_type.py
class ContainerCreateResponse(BaseModel, extra="allow"):
    id: Optional[str] = None
    created_at: Optional[int] = None
    name: Optional[str] = None
    object: Optional[str] = None
    status: Optional[str] = None
    expires_after: Optional[ExpiresAfter] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)
```

Key conventions:
- Use `BaseModel` with `extra="allow"` for forward compatibility
- All fields are `Optional` with `None` default
- Include `_headers` as `PrivateAttr()`
- Implement `__str__`, `__getitem__`, `get`, and `get_headers` methods

## Adding New Endpoints

### For OpenAI Wrapper Endpoints

1. Create wrapper class in `api_resources/apis/`:
   ```python
   class NewResource(APIResource):
       def __init__(self, client: Portkey):
           super().__init__(client)
           self.openai_client = client.openai_client
   ```

2. Create response types in `api_resources/types/`

3. Register in `client.py`:
   ```python
   self.new_resource = apis.NewResource(self)
   ```

4. Export in `api_resources/__init__.py` and `portkey_ai/__init__.py`

### For Portkey-Specific Endpoints

1. Create class using internal HTTP client:
   ```python
   class NewResource(APIResource):
       def create(self, **kwargs):
           return self._post(
               "/portkey/new-endpoint",
               body=body,
               cast_to=ResponseType,
               ...
           )
   ```

2. Follow same registration and export steps

## Portkey Headers

The SDK automatically adds Portkey-specific headers via `createHeaders()`:

- `x-portkey-api-key` - Portkey API key
- `x-portkey-virtual-key` - Virtual key for provider auth
- `x-portkey-config` - Gateway config
- `x-portkey-provider` - Target provider
- `x-portkey-trace-id` - Tracing ID
- `x-portkey-metadata` - Custom metadata
- Provider-specific headers (AWS, Azure, Vertex, etc.)

## Export Chain

Classes must be exported through the full chain:

```
api_resources/apis/new_resource.py     # Define class
        ↓
api_resources/apis/__init__.py         # Export from apis
        ↓
api_resources/__init__.py              # Re-export from api_resources
        ↓
portkey_ai/__init__.py                 # Final public export + add to __all__
```

## Updating Vendored OpenAI SDK

### Step-by-Step Process

#### Step 1: Compare SDK Versions
Before vendoring, compare changes between versions:
```
https://github.com/openai/openai-python/compare/vOLD...vNEW
```
This helps identify:
- New methods/resources added
- Removed/deprecated methods
- Signature changes in existing methods

#### Step 2: Clean and Re-vendor

```bash
# Delete the old vendor folder contents
rm -rf portkey_ai/_vendor/*

# Update version in vendorize.toml
packages = ["openai==X.Y.Z"]

# Run vendorize (install with: pip install vendorize)
python-vendorize
```

The tool rewrites imports from `openai.*` to `portkey_ai._vendor.openai.*`

#### Step 3: Apply Portkey Customizations

**Two files MUST be modified after every vendoring:**

1. **`portkey_ai/_vendor/openai/_constants.py`**
   ```python
   # Change DEFAULT_MAX_RETRIES from 2 to 1
   DEFAULT_MAX_RETRIES = 1
   ```

2. **`portkey_ai/_vendor/openai/_base_client.py`**
   
   Replace the `_should_retry` method with Portkey's custom logic:
   ```python
   def _should_retry(self, response: httpx.Response) -> bool:
       # Custom Retry Conditions
       retry_status_code = response.status_code
       retry_trace_id = response.headers.get("x-portkey-trace-id")
       retry_request_id = response.headers.get("x-portkey-request-id")
       retry_gateway_exception = response.headers.get("x-portkey-gateway-exception")

       if (
           retry_status_code < 500
           or retry_trace_id
           or retry_request_id
           or retry_gateway_exception
       ):
           return False

       return True
   ```

#### Step 4: Run Lint to Find Issues

```bash
make lint
```

This will surface:
- Type incompatibilities
- Missing imports
- Signature mismatches

#### Step 5: Update Portkey Wrappers

For each wrapper that needs updating:

**Adding new parameters:**
```python
# If wrapper explicitly lists parameters (not just **kwargs)
# Add new params with Union[Type, Omit] = omit pattern
def create(
    self,
    *,
    existing_param: Union[str, Omit] = omit,
    new_param: Union[str, Omit] = omit,  # Add new param
    **kwargs,
):
    response = self.openai_client.with_raw_response.resource.create(
        existing_param=existing_param,
        new_param=new_param,  # Pass to underlying client
        ...
    )
```

**Adding new methods:**
```python
def new_method(
    self,
    *,
    param: Union[str, Omit] = omit,
    **kwargs,
) -> NewResponseType:
    import json
    extra_headers = kwargs.pop("extra_headers", None)
    extra_query = kwargs.pop("extra_query", None)
    extra_body = kwargs.pop("extra_body", None)
    timeout = kwargs.pop("timeout", None)
    
    response = self.openai_client.with_raw_response.resource.new_method(
        param=param,
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body={**(extra_body or {}), **kwargs},
        timeout=timeout,
    )
    data = NewResponseType(**json.loads(response.text))
    data._headers = response.headers
    return data
```

**Adding new response types:**
```python
# In api_resources/types/
class NewResponseType(BaseModel, extra="allow"):
    id: str
    created_at: int
    # ... other fields from OpenAI type
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)
```

#### Step 6: Handle Type Ignore Comments

Sometimes Portkey uses more flexible types than OpenAI's strict literals:
```python
# Portkey allows any string, OpenAI expects specific literals
response = self.openai_client.with_raw_response.resource.method(
    model=model,  # type: ignore[arg-type]
    ...
)
```

#### Step 7: Verify and Test

```bash
# Format code
make format

# Run all checks
make lint

# Test imports
python -c "from portkey_ai import Portkey; print('OK')"

# Run tests (requires valid virtual keys)
pytest . -n 10
```

### Wrapper Resilience Pattern

Most Portkey wrappers use `**kwargs` pattern which automatically forwards new parameters:

```python
def create(self, *, name: str, **kwargs):
    extra_headers = kwargs.pop("extra_headers", None)
    # ... other pops
    response = self.openai_client.with_raw_response.resource.create(
        name=name,
        extra_headers=extra_headers,
        extra_body={**(extra_body or {}), **kwargs},  # Unknown params go here
    )
```

This means many new OpenAI parameters work automatically without code changes. Only add explicit parameters when:
1. The wrapper doesn't pass `**kwargs` to `extra_body`
2. You want IDE autocomplete/type hints for important params
3. The parameter needs special handling

### Checklist for Vendoring

- [ ] Delete `portkey_ai/_vendor/*`
- [ ] Update `vendorize.toml` with new version
- [ ] Run `python-vendorize`
- [ ] Set `DEFAULT_MAX_RETRIES = 1` in `_constants.py`
- [ ] Replace `_should_retry` in `_base_client.py`
- [ ] Run `make lint` and fix errors
- [ ] Add new methods/types if needed
- [ ] Run `make format`
- [ ] Test imports work
- [ ] Commit vendored code first, then wrapper changes

## Common Gotchas

1. **Don't use `Optional[X]` for omittable params** - Use `Union[X, Omit]` instead
2. **Always use `with_raw_response`** for non-streaming calls to access headers
3. **Streaming calls cannot use `with_raw_response`** - Return the stream directly
4. **Remember both sync and async versions** - Every class needs `Async` counterpart
5. **Extra kwargs go to `extra_body`** - Any unknown kwargs are merged into extra_body
6. **FileTypes comes from vendor** - Use `from ..._vendor.openai._types import FileTypes`
7. **Response parsing uses `json.loads(response.text)`** - Not `response.json()`
