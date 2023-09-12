
import portkey as pk
from portkey import Config, LLMOptions
from getpass import getpass

# Enter the password on the prompt window.
API_KEY = "x2trk"

# Setting the API key
pk.api_key = API_KEY

pk.config = Config(
    mode="fallback",
    llms=[
        LLMOptions(virtual_key="open-ai-key-66a67d", provider="openai"),
        LLMOptions(virtual_key="anthropic-key-351feb", provider="anthropic")
    ]
)


response = pk.Completions.create(
    model="text-davinci-002",
    prompt="Who are you ?"
)

print(response.choices[0].text)