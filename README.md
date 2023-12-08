<div align="center">
<img src="https://assets.portkey.ai/header.png" height=150><br />

## Build reliable, secure, and production-ready AI apps easily.

```bash
pip install portkey-ai
```
</div>

## **💡 Features**

**🚪 AI Gateway:**
*  Unified API Signature: If you've used OpenAI, you already know how to use Portkey with any other provider.
*  Interoperability: Write once, run with any provider. Switch between _any model_ from _any provider_ seamlessly. 
*  Automated Fallbacks & Retries: Ensure your application remains functional even if a primary service fails.
*  Load Balancing: Efficiently distribute incoming requests among multiple models.
*  Semantic Caching: Reduce costs and latency by intelligently caching results.

**🔬 Observability:**
*  Logging: Keep track of all requests for monitoring and debugging.
*  Requests Tracing: Understand the journey of each request for optimization.
*  Custom Tags: Segment and categorize requests for better insights.


## **🚀 Quick Start**

#### First, install the SDK & export Portkey API Key
[Get Portkey API key here.](https://app.portkey.ai/signup)
```bash
$ pip install portkey-ai
$ export PORTKEY_API_KEY=PORTKEY_API_KEY
```

#### Now, let's make a request with GPT-4

```py
from portkey_ai import Portkey

# Construct a client with a virtual key
portkey = Portkey(
    api_key="PORTKEY_API_KEY",
    virtual_key="VIRTUAL_KEY"
)

completion = portkey.chat.completions.create(
    messages = [{ "role": 'user', "content": 'Say this is a test' }],
    model = 'gpt-3.5-turbo'
)
print(completion)
```

Portkey fully adheres to the OpenAI SDK signature. This means that you can instantly switch to Portkey and start using Portkey's advanced production features right out of the box.


## **🤝 Supported Providers**

|| Provider  | Support Status  | Supported Endpoints |
|---|---|---|---|
| <img src="https://assets.portkey.ai/openai.png" width=18 />| OpenAI | ✅ Supported  | `/completion`, `/embed` |
| <img src="https://assets.portkey.ai/azure.png" width=18>| Azure OpenAI | ✅ Supported  | `/completion`, `/embed` |
| <img src="https://assets.portkey.ai/anthropic.png" width=18>| Anthropic  | ✅ Supported  | `/complete` |
| <img src="https://assets.portkey.ai/anyscale.png" width=18>| Anyscale  | ✅ Supported  | `/chat/completions` |
| <img src="https://assets.portkey.ai/cohere.png" width=18>| Cohere  | 🚧 Coming Soon  | `generate`, `embed` |


---

#### [📝 Full Documentation](https://docs.portkey.ai/) | [🛠️ Integration Requests](https://github.com/Portkey-AI/portkey-python-sdk/issues) | 

<a href="https://twitter.com/intent/follow?screen_name=portkeyai"><img src="https://img.shields.io/twitter/follow/portkeyai?style=social&logo=twitter" alt="follow on Twitter"></a>
<a href="https://discord.gg/sDk9JaNfK8" target="_blank"><img src="https://img.shields.io/discord/1143393887742861333?logo=discord" alt="Discord"></a>

## **🛠️ Contributing**
Get started by checking out Github issues. Feel free to open an issue, or reach out if you would like to add to the project!