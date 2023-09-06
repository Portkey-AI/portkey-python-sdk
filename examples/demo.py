from portkey import Portkey, LLMBase, DefaultParams, Message


messages = [
    Message(role="system", content="You are a helpful assistant"),
    Message(role="user", content="What can you do?"),
]
client = Portkey(
    base_url="https://api.portkeydev.com",
    default_params=DefaultParams(
        prompt="What can you do?",
        max_tokens=250,
    ),
)

openai_llm = LLMBase(provider="openai", model="text-davinci-003", cache_status="simple")
response = client.completion.with_fallbacks(llms=[openai_llm], stream=True)

# print(response.choices[0]["text"])
for i in response:
    print(i.choices[0].get("text"), end="", flush=True)
