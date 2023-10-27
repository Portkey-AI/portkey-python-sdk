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
import portkey
from portkey import Config, LLMOptions

portkey.config = Config(
    mode="single",
    llms=LLMOptions(provider="openai", api_key="OPENAI_API_KEY")
)

r = portkey.ChatCompletions.create(
    model="gpt-4", 
    messages=[
        {"role": "user","content": "Hello World!"}
    ]
)
```

Portkey fully adheres to the OpenAI SDK signature. This means that you can instantly switch to Portkey and start using Portkey's advanced production features right out of the box.


## **🪜 Detailed Integration Guide**

**4 Steps to Integrate the SDK**
1. Get your virtual key for AI providers.
2. Construct your LLM, add Portkey features, provider features, and prompt.
3. Construct the Portkey client and set your usage mode.
4. Now call Portkey regularly like you would call your OpenAI constructor.

Let's dive in! If you are an advanced user and want to directly jump to various full-fledged examples, [click here](https://github.com/Portkey-AI/portkey-python-sdk/tree/main/examples).

---

### **Step 1️⃣ : Get your Virtual Keys for AI providers**

Navigate to the "Virtual Keys" page on [Portkey](https://app.portkey.ai/) and hit the "Add Key" button. Choose your AI provider and assign a unique name to your key. Your virtual key is ready!

### **Step 2️⃣ : Construct your LLM, add Portkey features, provider features, and prompt**

**Portkey Features**:
You can find a comprehensive [list of Portkey features here](#📔-list-of-portkey-features). This includes settings for caching, retries, metadata, and more.

**Provider Features**:
Portkey is designed to be flexible. All the features you're familiar with from your LLM provider, like `top_p`, `top_k`, and `temperature`, can be used seamlessly. Check out the [complete list of provider features here](https://github.com/Portkey-AI/portkey-python-sdk/blob/af0814ebf4f1961b5dfed438918fe68b26ef5f1e/portkey/api_resources/utils.py#L137).

**Setting the Prompt Input**:
This param lets you override any prompt that is passed during the completion call - set a model-specific prompt here to optimise the model performance. You can set the input in two ways. For models like Claude and GPT3, use `prompt` = `(str)`, and for models like GPT3.5 & GPT4, use `messages` = `[array]`.


Here's how you can combine everything:

```python
from portkey import LLMOptions

# Portkey Config
provider = "openai"
virtual_key = "key_a"
trace_id = "portkey_sdk_test"

# Model Settings
model = "gpt-4"
temperature = 1

# User Prompt
messages = [{"role": "user", "content": "Who are you?"}]

# Construct LLM
llm = LLMOptions(provider=provider, virtual_key=virtual_key, trace_id=trace_id, model=model, temperature=temperature)
```

### **Step 3️⃣ : Construct the Portkey Client**

Portkey client's config takes 3 params: `api_key`, `mode`, `llms`.

* `api_key`: You can set your Portkey API key here or with `os.ennviron` as done above.
* `mode`: There are **3** modes - Single, Fallback, Loadbalance.
  * **Single** - This is the standard mode. Use it if you do not want Fallback OR Loadbalance features.
  * **Fallback** - Set this mode if you want to enable the Fallback feature.
  * **Loadbalance** - Set this mode if you want to enable the Loadbalance feature. 
* `llms`: This is an array where we pass our LLMs constructed using the LLMOptions constructor.

```py
import portkey
from portkey import Config

portkey.config = Config(mode="single",llms=[llm])
```

### **Step 4️⃣ : Let's Call the Portkey Client!**

The Portkey client can do `ChatCompletions` and `Completions`.

Since our LLM is GPT4, we will use ChatCompletions:

```py
response = portkey.ChatCompletions.create(
    messages=[{
      "role": "user",
      "content": "Who are you ?"
    }]
)
print(response.choices[0].message)
```

You have integrated Portkey's Python SDK in just 4 steps!

---

## **🔁 Demo: Implementing GPT4 to GPT3.5 Fallback Using the Portkey SDK**

```py
import os
os.environ["PORTKEY_API_KEY"] = "PORTKEY_API_KEY" # Setting the Portkey API Key

import portkey
from portkey import Config, LLMOptions

# Let's construct our LLMs.
llm1 = LLMOptions(provider="openai", model="gpt-4", virtual_key="key_a"),
llm2 = LLMOptions(provider="openai", model="gpt-3.5-turbo", virtual_key="key_a")

# Now let's construct the Portkey client where we will set the fallback logic
portkey.config = Config(mode="fallback",llms=[llm1,llm2])

# And, that's it!
response = portkey.ChatCompletions.create()
print(response.choices[0].message)
```

## **📔 Full List of Portkey Config**

| Feature             | Config Key              | Value(Type)                                      | Required    |
|---------------------|-------------------------|--------------------------------------------------|-------------|
| Provider Name       | `provider`        | `string`                                         | ✅ Required  |
| Model Name        | `model`        | `string`                                         | ✅ Required |
| Virtual Key OR API Key        | `virtual_key` or `api_key`        | `string`                                         | ✅ Required (can be set externally) |
| Cache Type          | `cache_status`          | `simple`, `semantic`                             | ❔ Optional |
| Force Cache Refresh | `cache_force_refresh`   | `True`, `False` (Boolean)                                 | ❔ Optional |
| Cache Age           | `cache_age`             | `integer` (in seconds)                           | ❔ Optional |
| Trace ID            | `trace_id`              | `string`                                         | ❔ Optional |
| Retries         | `retry`           | `{dict}` with two required keys: `"attempts"` which expects integers in [0,5] and `"on_status_codes"` which expects array of status codes like [429,502] <br> `Example`: { "attempts": 5, "on_status_codes":[429,500] }                      | ❔ Optional |
| Metadata            | `metadata`              | `json object` [More info](https://docs.portkey.ai/key-features/custom-metadata)          | ❔ Optional |


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