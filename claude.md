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
│   │   └── openai/              # Vendored OpenAI SDK (e.g., v2.7.1)
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
packages = ["openai==2.7.1"]
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

1. Update version in `vendorize.toml`:
   ```toml
   packages = ["openai==X.Y.Z"]
   ```

2. Run vendorize tool (typically `vendorize` or `python -m vendorize`)

3. The tool rewrites imports from `openai.*` to `portkey_ai._vendor.openai.*`

4. After vendoring:
   - Check for new OpenAI resources that need Portkey wrappers
   - Update any Portkey types that mirror OpenAI types
   - Test thoroughly - OpenAI SDK changes can break wrappers

## Common Gotchas

1. **Don't use `Optional[X]` for omittable params** - Use `Union[X, Omit]` instead
2. **Always use `with_raw_response`** for non-streaming calls to access headers
3. **Streaming calls cannot use `with_raw_response`** - Return the stream directly
4. **Remember both sync and async versions** - Every class needs `Async` counterpart
5. **Extra kwargs go to `extra_body`** - Any unknown kwargs are merged into extra_body
6. **FileTypes comes from vendor** - Use `from ..._vendor.openai._types import FileTypes`
7. **Response parsing uses `json.loads(response.text)`** - Not `response.json()`
