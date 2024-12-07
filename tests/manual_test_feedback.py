import os
from portkey_ai import Portkey


portkey = Portkey(
    api_key=os.environ.get("PORTKEY_API_KEY"),
)


traceId = "<trace_id>"


print("Step: Create Feedback")
result = portkey.feedback.create(
    trace_id=traceId,
    value="1",
)
print(result)


print("Step: Update Feedback")
result = portkey.feedback.update(
    feedback_id=traceId,
    value="7",
)
print(result)
