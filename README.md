<img src="https://raw.githubusercontent.com/Portkey-AI/Rubeus/main/docs/images/header.png" width=2000>

<div align="center">
<br />
  <a href="https://discord.gg/sDk9JaNfK8" target="_blank">
      <img src="https://img.shields.io/discord/1143393887742861333?logo=discord" alt="Discord">
  </a>
    <a href="https://github.com/Portkey-AI/rubeus-python-sdk/blob/main/LICENSE" target="_blank">
      <img src="https://img.shields.io/static/v1?label=license&message=MIT&color=blue" alt="License">
  </a> 
  <a href="https://pypi.org/project/rubeus/" target="_blank">
      <img src="https://img.shields.io/pypi/pyversions/ubeus" alt="PyPi">
  </a> 
    <br />
    <a href="https://docs.portkey.ai/" target="_blank">
      <img src="https://img.shields.io/static/v1?label=📝 &message=docs&color=grey" alt="docs">
  </a> 
    <a href="https://docs.portkey.ai/" target="_blank">
      <img src="https://img.shields.io/static/v1?label=🦙 &message=llamaindex&color=grey" alt="llamaindex">
  </a> 
    <a href="https://docs.portkey.ai/" target="_blank">
      <img src="https://img.shields.io/static/v1?label=🦜🔗 &message=langchain&color=grey" alt="langchain">
  </a> 
  <br />
      <a href="https://docs.portkey.ai/" target="_blank">
    <img src="https://colab.research.google.com/assets/colab-badge.svg" alt=\"Open In Colab\"/>
  </a> 
    <a href="https://twitter.com/intent/follow?screen_name=portkeyai">
        <img src="https://img.shields.io/twitter/follow/portkeyai?style=social&logo=twitter"
            alt="follow on Twitter">
    </a>
</div>

---

#### **Rubeus** streamlines API requests to 20+ LLMs. It provides a unified API signature for interacting with all LLMs alongwith powerful LLM Gateway features like load balancing, fallbacks, retries and more. 

```bash
pip install rubeus
```

### 💡 Features

|| Name | Description | Example |
|---|---|---|---|
| 🌐    | Interoperability       | Write once, run with any provider. Switch between __ models from __ providers seamlessly.               | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://docs.portkey.ai/) |
| 🔀    | Fallback Strategies    | Don't let failures stop you. If one provider fails, Rubeus can automatically switch to another.          | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://docs.portkey.ai/) |
| 🔄    | Retry Strategies       | Temporary issues shouldn't mean manual re-runs. Rubeus can automatically retry failed requests.         | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://docs.portkey.ai/) |
| ⚖️    | Load Balancing         | Distribute load effectively across multiple API keys or providers based on custom weights.              | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://docs.portkey.ai/) |
| 📝    | Unified API Signature  | If you've used OpenAI, you already know how to use Rubeus with any other provider.                      | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://docs.portkey.ai/) |

---

### 🤝 Supported Providers

|| Provider  | Support Status  | Supported Endpoints |
|---|---|---|---|
| <img src="docs/images/openai.png" width=18 />| OpenAI | ✅ Supported  | `/completion`, `/embed` |
| <img src="docs/images/azure.png" width=18>| Azure OpenAI | ✅ Supported  | `/completion`, `/embed` |
| <img src="docs/images/anthropic.png" width=18>| Anthropic  | ✅ Supported  | `/complete` |
| <img src="docs/images/cohere.png" width=18>| Cohere  | ✅ Supported  | `generate`, `embed` |
| <img src="docs/images/bard.png" width=18>| Google Bard  | 🚧 Coming Soon  |  |
| <img src="docs/images/localai.png" width=18>| LocalAI  | 🚧 Coming Soon  |  |

---

#### [📝 Full Documentation](https://github.com/Portkey-AI/rubeus-python-sdk) | [🎯 Roadmap](https://github.com/Portkey-AI/Rubeus/issues) | [🐞 Bug Reports](https://github.com/Portkey-AI/Rubeus/issues) | [💡 Feature Requests](https://github.com/Portkey-AI/Rubeus/issues)

#### 📞 Talk to the devs: [Rohit](https://twitter.com/jumbld) | [Ayush](https://twitter.com/ayushgarg_xyz)

