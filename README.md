<div align="center">
<img src="https://assets.portkey.ai/header.png" height=150><br />

## Control Panel for AI Apps
```bash
pip install portkey-ai
```

</div>

## Features

The Portkey SDK is built on top of the OpenAI SDK, allowing you to seamlessly integrate Portkey's advanced features while retaining full compatibility with OpenAI methods. With Portkey, you can enhance your interactions with OpenAI or any other OpenAI-like provider by leveraging robust monitoring, reliability, prompt management, and more features - without modifying much of your existing code.

### AI Gateway
<table>
    <tr>
        <td width=50%><b>Unified API Signature</b><br />If you've used OpenAI, you already know how to use Portkey with any other provider.</td>
        <td><b>Interoperability</b><br />Write once, run with any provider. Switch between any model from_any provider seamlessly. </td>
    </tr>
    <tr>
        <td width=50%><b>Automated Fallbacks & Retries</b><br />Ensure your application remains functional even if a primary service fails.</td>
        <td><b>Load Balancing</b><br />Efficiently distribute incoming requests among multiple models.</td>
    </tr>
    <tr>
        <td width=50%><b>Semantic Caching</b><br />Reduce costs and latency by intelligently caching results.</td>
        <td><b>Virtual Keys</b><br />Secure your LLM API keys by storing them in Portkey vault and using disposable virtual keys.</td>
    </tr>
    <tr>
        <td width=50%><b>Request Timeouts</b><br />Manage unpredictable LLM latencies effectively by setting custom request timeouts on requests.</td>
    </tr>
</table>

### Observability
<table width=100%>
    <tr>
        <td width=50%><b>Logging</b><br />Keep track of all requests for monitoring and debugging.</td>
        <td width=50%><b>Requests Tracing</b><br />Understand the journey of each request for optimization.</td>
    </tr>
    <tr>
        <td width=50%><b>Custom Metadata</b><br />Segment and categorize requests for better insights.</td>
        <td width=50%><b>Feedbacks</b><br />Collect and analyse weighted feedback on requests from users.</td>
    </tr>
    <tr>
        <td width=50%><b>Analytics</b><br />Track your app & LLM's performance with 40+ production-critical metrics in a single place.</td>
    </tr>
</table> 

## Usage

#### Prerequisites
1. [Sign up on Portkey](https://app.portkey.ai/) and grab your Portkey API Key
2. Add your [OpenAI key](https://platform.openai.com/api-keys) to Portkey's Virtual Keys page and keep it handy

```bash
# Installing the SDK

$ pip install portkey-ai
$ export PORTKEY_API_KEY=PORTKEY_API_KEY
```

#### Making a Request to OpenAI
* Portkey fully adheres to the OpenAI SDK signature. You can instantly switch to Portkey and start using our production features right out of the box. <br />
* Just replace `from openai import OpenAI` with `from portkey_ai import Portkey`:
```py
from portkey_ai import Portkey

portkey = Portkey(
    api_key="PORTKEY_API_KEY",
    virtual_key="VIRTUAL_KEY"
)

chat_completion = portkey.chat.completions.create(
    messages = [{ "role": 'user', "content": 'Say this is a test' }],
    model = 'gpt-4'
)

print(chat_completion)
```

#### Async Usage
* Use `AsyncPortkey` instead of `Portkey` with `await`:
```py
import asyncio
from portkey_ai import AsyncPortkey

portkey = AsyncPortkey(
    api_key="PORTKEY_API_KEY",
    virtual_key="VIRTUAL_KEY"
)

async def main():
    chat_completion = await portkey.chat.completions.create(
        messages=[{'role': 'user', 'content': 'Say this is a test'}],
        model='gpt-4'
    )

    print(chat_completion)

asyncio.run(main())
```

### Strands Agents Integration (optional)

Installation:

```bash
pip install 'portkey-ai[strands]'
```

Usage with Strands:

```python
from strands.agent import Agent
from portkey_ai.integrations.strands import PortkeyStrands

model = PortkeyStrands(
    api_key="PORTKEY_API_KEY",
    model_id="@openai/gpt-4o-mini",
#   base_url="https://api.portkey.ai/v1",  ## Optional    
)

agent = Agent(model=model)

## Now, use your agent as usual
```

### Google ADK Integration (optional)

Installation:

```bash
pip install 'portkey-ai[adk]'
```

Usage with ADK:

```python
import asyncio
from google.adk.models.llm_request import LlmRequest
from google.genai import types
from portkey_ai.integrations.adk import PortkeyAdk

llm = PortkeyAdk(
    api_key="PORTKEY_API_KEY",
    model="@openai/gpt-4o-mini",
#   base_url="https://api.portkey.ai/v1",  ## Optional    
)

req = LlmRequest(
    model="@openai/gpt-4o-mini",
    contents=[
        types.Content(
            role="user",
            parts=[types.Part.from_text("Tell me a short programming joke.")],
        )
    ],
)

async def main():
    async for resp in llm.generate_content_async(req, stream=True):
        if resp.content and resp.content.parts:
            for p in resp.content.parts:
                if getattr(p, "text", None):
                    print(p.text, end="")
    print()

asyncio.run(main())
```

Configuration notes:

- **system_role**: By default, the adapter sends the system instruction as a `developer` role message to align with ADK/LiteLLM. If your provider expects a strict `system` role, pass `system_role="system"` when constructing `PortkeyAdk`.
  
  ```python
  llm = PortkeyAdk(
      model="gpt-4o-mini",
      api_key="PORTKEY_API_KEY",
      system_role="system",  # switch from default "developer"
  )
  ```

- **Tools**: When tools are present in the ADK request, the adapter sets `tool_choice="auto"` to enable function calling by default (mirrors the Strands adapter behavior).

## Compatibility with OpenAI SDK

Portkey currently supports all the OpenAI methods, including the legacy ones.

| Methods                    | OpenAI<br>V1.26.0 | Portkey<br>V1.3.1 |
|:----------------------------|:--------|:---------|
| [Audio](https://portkey.ai/docs/product/ai-gateway-streamline-llm-integrations/multimodal-capabilities/vision-1) | ✅ | ✅ |
| [Chat](https://portkey.ai/docs/api-reference/chat-completions) | ✅ | ✅ |
| [Embeddings](https://portkey.ai/docs/api-reference/embeddings) | ✅ | ✅ |
| [Images](https://portkey.ai/docs/api-reference/completions-1) | ✅ | ✅ |
| Fine-tuning                  | ✅     | ✅      |
| Batch                        | ✅     | ✅      |
| Files                        | ✅     | ✅      |
| Models                       | ✅     | ✅      |
| Moderations                  | ✅     | ✅      |
| Assistants                   | ✅     | ✅      |
| Threads                      | ✅     | ✅      |
| Thread - Messages            | ✅     | ✅      |
| Thread - Runs                | ✅     | ✅      |
| Thread - Run - Steps         | ✅     | ✅      |
| Vector Store                 | ✅     | ✅      |
| Vector Store - Files         | ✅     | ✅      |
| Vector Store - Files Batches | ✅     | ✅      |
| Generations                  | ❌ (Deprecated) | ✅ |
| Completions                  | ❌ (Deprecated) | ✅ |

### Portkey-Specific Methods
| Methods | Portkey<br>V1.3.1 |
| :-- | :-- |
| [Feedback](https://portkey.ai/docs/api-reference/feedback) | ✅ |
| [Prompts](https://portkey.ai/docs/api-reference/prompts) | ✅ |

---

#### [Check out Portkey docs for the full list of supported providers](https://portkey.ai/docs/welcome/what-is-portkey#ai-providers-supported)

<a href="https://twitter.com/intent/follow?screen_name=portkeyai"><img src="https://img.shields.io/twitter/follow/portkeyai?style=social&logo=twitter" alt="follow on Twitter"></a>
<a href="https://discord.gg/sDk9JaNfK8" target="_blank"><img src="https://img.shields.io/discord/1143393887742861333?logo=discord" alt="Discord"></a>

#### Contributing
Get started by checking out Github issues. Email us at support@portkey.ai or just ping on Discord to chat.
