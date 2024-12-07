import asyncio
from portkey_ai import AsyncPortkey
import os


portkey = AsyncPortkey(
    api_key=os.environ.get("PORTKEY_API_KEY"),
)


traceId = "0c41ce35-b321-4484-bead-1c21eae02996"


async def main():
    print("Step: Create Feedback")
    result = await portkey.feedback.create(
        trace_id=traceId,
        value="1",
    )
    print(result)

    update_feedback_id = result.feedback_ids[0]

    print("Step: Update Feedback")
    result = await portkey.feedback.update(
        feedback_id=update_feedback_id,
        value="7",
    )
    print(result)


asyncio.run(main())
