import os
from portkey_ai import Portkey

portkey = Portkey(
    api_key="Xgv7++HhSeF70UzdVSsmtJuGYe0=",
    virtual_key="portkey-welcome-e248d3"
)


file_name = "./tests/configs/batches/seed_tasks.jsonl"


print("Step 1: Create a batch file")
batch_file = portkey.files.create(
  file=open(file_name, "rb"),
  purpose="batch"
)
print(batch_file)


print("Step 2: Create a batch job")
batch_job = portkey.batches.create(
  input_file_id=batch_file.id,
  endpoint="/v1/chat/completions",
  completion_window="24h"
)
print(batch_job)

print("Step 3: Retrieve the batch job")
batch_job = portkey.batches.retrieve(batch_job.id)
print(batch_job)


print("Step 4: Retrieve the result")
result_file_id = batch_job.output_file_id
result = portkey.files.content(result_file_id).content
print(result)