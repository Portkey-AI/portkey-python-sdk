from rubeus import Rubeus, LLMBase, DefaultParams

client = Rubeus(
    default_params=DefaultParams(
        messages=[
            {
                "role": "user",
                "content": "What are the top 10 happiest countries in the world?",
            }
        ],
        max_tokens=50,
        stream=True,
    )
)

openai_llm = LLMBase(provider="openai", model="gpt-3.5-turbo")
response = client.chat_completion.with_fallbacks(llms=[openai_llm], stream=True)

print(response)
for i in response:
    print(i.choices)
