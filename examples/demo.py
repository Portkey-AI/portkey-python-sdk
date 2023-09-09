import portkey
from portkey import Config, LLMBase, Message, Params

# portkey.api_key = ""
# portkey.base_url = ""

messages = [
    Message(role="system", content="You are a helpful assistant"),
    Message(role="user", content="What can you do?"),
]
portkey.config = Config(
    mode="fallback",
    llms=[
        LLMBase(
            provider="openai",
            model="gpt-3.5-turbo",
            max_tokens=250,
            messages=messages,
        ),
        LLMBase(
            provider="anthropic",
            model="claude-2",
            max_tokens=250,
        ),
    ],
)

response = portkey.ChatCompletions.create(
    stream=True, virtual_key="pk-virtualkey-12345", temperature=0
)
for i in response:
    print(i.choices[0].get("delta", {}).get("content"), end="", flush=True)
