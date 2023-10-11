import os

# pk.api_key = "nOlf96qHHgE7fcJaXNpVi6TesNs="
# pk.base_url = "https://api.portkeydev.com"

# # # Setting the config for portkey
# pk.config = Config(
#     mode="fallback",
#     llms=[
#        LLMOptions(virtual_key="open-ai-key-b395a0", provider="openai")
#     ]
# )

# response3 = pk.ChatCompletions.create(
#     messages=[{"role": "user", "content": "Write an essay on India"}],
#     stream=True,  # Stream back partial progress
#     max_tokens=2000
# )

# count = 0

# for event in response3:
#     count +=1
#     if len(event.choices) == 0:
#         continue
#     if event.choices[0].delta is None:
#         break
#     print(event.choices[0].delta.get("content", ""), end="", flush=True)

# # response = pk.Generations.create(
# #     prompt_id="86c653fc-1d89-4c88-90a7-f579aa242e0d",
# #     variables = {
# #         "question": "Why is the sky blue ?",
# #         "context": "You're a helpfull assistant"
# #     }
# # )

# # print(response.data)

# # response2 = pk.Completions.create(
# #     model="text-davinci-002",
# #     prompt="Tell me a story",
# #     max_tokens=2000,  # Limit the generated text to 100 tokenn
# # )

# # print(response2)


import portkey

# base_url = os.environ.get("API_BASE_URL", "https://api.portkey.ai")
# api_key = os.environ.get("PORTKEY_API_KEY", "/turdjWE+tIUeAzmzGxGEkkJLBQ=")

# client = portkey
# client.api_key = api_key
# config = Config(
#     mode="single",
# )
# client.config = config
# _ = client.Generations.create(prompt_id="22a96a48-95ef-47cd-84a8-fd37c7930313")
# print(completion)
# for i in completion:
#     if 'text' in i.choices[0]:
#         print(i.choices[0]['text'], end="", flush=True)

from dotenv import load_dotenv

client = portkey

# # from tests.utils import assert_matches_type
load_dotenv()
base_url = os.environ.get("PORTKEY_BASE_URL")
api_key = os.environ.get("PORTKEY_API_KEY")
virtual_api_key = os.environ.get("OPENAI_VIRTUAL_KEY")
anyscale_api_key = os.environ.get("ANYSCALE_API_KEY")


# config = Config(
#     mode="single",
#     llms=LLMOptions(
#         virtual_key=virtual_api_key,
#         provider="openai",
#         model="text-davinci-002",

#     ),
# )
# client.config = config
# # _ = client.ChatCompletions.create(
# #     max_tokens=300,
# #     messages=[{"role": "user", "content": "Tell me a story"}],
# #     stream=False,
# #     temperature=1,
# #     top_k=5,
# #     top_p=0.7
# # )

# res = pk.Completions.create(
#     prompt="Tell me a story",
# )

# print(res)

print(base_url, api_key)
print("Starts now...")
# config = Config(
#             mode="single",
#             llms=LLMOptions(
#                 api_key=anyscale_api_key,
#                 provider="anyscale",
#                 metadata={"_user": "portkey-python-sdk", '_environment': "localDev"},
#                 model="codellama/CodeLlama-34b-Instruct-hf",
#                 trace_id="7364t7346rt4"
#             ),
#         )
# client.config = "pc-config-6c7422"
# client.api_key = api_key
# client.base_url = base_url
# _ = client.ChatCompletions.create(
#     max_tokens=100,
#     messages=[{"role": "user", "content": "Who is the first president of America1 ?"}],
#     stream=True
# )

client.config = "pc-config-6c7422"
completion = client.ChatCompletions.create(
    messages=[{"role": "user", "content": "Who is the first president of America1 ?"}],
    stream=True,
)


for res in completion:
    print(res.choices[0].delta.get("content", ""), end="", flush=True)
