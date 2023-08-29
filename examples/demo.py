from rubeus import Rubeus, LLMBase

client = Rubeus(
    default_params={
        "messages": [
            {
                "role": "user",
                "content": "What are the top 10 happiest countries in the world?",
            }
        ],
        "max_tokens": 50,
    },
)

openai_llm = LLMBase(provider="openai", model="gpt-3.5-turbo")
res = client.chat_completion.with_fallbacks(llms=[openai_llm])

print(res)
