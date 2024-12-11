import os
from portkey_ai import Assistants, Messages, Portkey, Uploads

# Initialize the Portkey client
portkey = Portkey(
    api_key=os.environ.get("PORTKEY_API_KEY"),
    virtual_key=os.environ.get("OPENAI_VIRTUAL_KEY"),
)

file_to_upload_path = "./tests/configs/threads/sample.pdf"


def test_upload_file_and_query() -> None:
    print("Step 1: Create Assistant")
    assistant = Assistants(portkey).create(
        model="gpt-4o-mini",
        description="for testing purposes",
        tools=[{"type": "file_search"}],
    )
    print(assistant)

    print("Step 2: Create Upload")
    upload = Uploads(portkey).create(
        purpose="assistants",
        bytes=os.stat(file_to_upload_path).st_size,  # get total bytes
        filename=file_to_upload_path.split("/")[-1],
        mime_type="application/pdf",
    )
    print(upload)

    print("Step 3: Create one or more parts for the upload_id received from step 1")
    part = Uploads(portkey).parts.create(
        data=open(file_to_upload_path, "rb").read(), upload_id=upload.id
    )
    print(part)

    print("Step 4: Complete the upload")
    complete_upload = Uploads(portkey).complete(upload_id=upload.id, part_ids=[part.id])
    print(complete_upload)

    print("Step 5: Create a run and poll")
    run = portkey.beta.threads.create_and_run_poll(
        thread={
            "messages": [
                {
                    "role": "user",
                    "content": "What is this document about?",
                    # Attach the new file to the message.
                    "attachments": [
                        {
                            "file_id": complete_upload.file.id,
                            "tools": [{"type": "file_search"}],
                        }
                    ],
                }
            ]
        },
        assistant_id=assistant.id,
    )
    print(run)

    print("Step 6: Get the list of the messages")
    messages = Messages(portkey).list(thread_id=run.thread_id)
    print(messages)
