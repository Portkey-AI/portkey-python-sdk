from portkey import Portkey, LLMBase, DefaultParams, Message


messages = [
    Message(role="system", content="You are a helpful assistant"),
    Message(role="user", content="What can you do?"),
]
client = Portkey(
    default_params=DefaultParams(
        messages=messages,
        max_tokens=50,
        stream=True,
    )
)

openai_llm = LLMBase(provider="openai", model="gpt-3.5-turbo")
response = client.chat_completion.with_fallbacks(llms=[openai_llm], stream=True)

print(response)
for i in response:
    print(i.choices)
