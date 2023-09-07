import portkey
from portkey import Config, LLMBase, Message, Params

portkey.api_key = ""
portkey.base_url = ""

messages = [
    Message(role="system", content="You are a helpful assistant"),
    Message(role="user", content="What can you do?"),
]
# portkey.mode = "loadbalance"
config = Config(
    mode="loadbalance",
    llms=[
        LLMBase(
            provider="openai", model="gpt-3.5-turbo", max_tokens=250, messages=messages,
            api_key=""),
        LLMBase(provider="anthropic", model="claude-2", max_tokens=250,),],
    params=Params(messages=messages),)

response = portkey.ChatCompletions.create(config=config, stream=True)
# portkey.Completions.create()
for i in response:
    print(i.choices[0].get("delta", {}).get("content"), end="", flush=True)
