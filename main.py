from io import BytesIO
import os
from dotenv import load_dotenv
import openai
import json
import time
import logging
from datetime import datetime
import streamlit as st

load_dotenv()

client = openai.OpenAI()

model = "gpt-4-1106-preview"

# Harcoded ids to be used once the first code run is done
thread_id = "" # YOUR OWN THREAD ID
assis_id = "" # YOUR OWN ASSIST IF

# Initialize all the session
if "file_id_list" not in st.session_state:
    st.session_state.file_id_list = []

if "start_chat" not in st.session_state:
    st.session_state.start_chat = False

if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

if "vector_store_id" not in st.session_state:
    st.session_state.vector_store_id = None

# Set up our frontend page
st.set_page_config(
    page_title="Study Budy - chat and learn",
    page_icon=":books:",
)


# Function definitions
def upload_file_to_vector_store(file_name, file_stream):
    # Upload file only if it hasn't been uploaded yet
    if file_name not in [f[0] for f in st.session_state.file_id_list]:
        file_streams = [(file_name, file_stream)]
        file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=st.session_state.vector_store_id, files=file_streams
        )
        st.session_state.file_id_list.append((file_name, file_streams))
        
# Sidebar - where users can upload files
file_uploaded = st.sidebar.file_uploader(
    "Upload a file to be transformed into embeddings", key="file_uploaded"
)

# Create or retrieve the Vector store id
if st.session_state.vector_store_id is None:
    vector_store = client.beta.vector_stores.create(name="PDF Interaction")
    st.session_state.vector_store_id = vector_store.id
else:
    vector_store = client.beta.vector_stores.retrieve(st.session_state.vector_store_id)

# Upload file button - store file ID
if file_uploaded:
    # Lire le contenu du fichier téléchargé en mode binaire
    file_stream = file_uploaded.read()
    file_name = file_uploaded.name
    upload_file_to_vector_store(file_name, file_stream)
    st.sidebar.write(f"Files uploaded and added to Vector Store: {file_name}")

# Display uploaded file IDs
if st.session_state.file_id_list:
    st.sidebar.write("Uploaded file IDs:")
    for file in st.session_state.file_id_list:
        st.sidebar.write(file[0])
    assistant = client.beta.assistants.update(
        assistant_id=assis_id,
        tool_resources={
            "file_search": {"vector_store_ids": [st.session_state.vector_store_id]}
        },
    )

# Button to initiate the chat session
if st.sidebar.button("Start Chatting..."):
    if st.session_state.file_id_list:
        st.session_state.start_chat = True
        if st.session_state.thread_id is None:
            chat_thread = client.beta.threads.create()
            st.session_state.thread_id = chat_thread.id
        st.write("Thread ID:", st.session_state.thread_id)
    else:
        st.sidebar.warning(
            "No files found. Please upload at least one file to get started!"
        )

# Define the function to process messages with citations
def process_message_with_citations(message):
    """Extract content and annotations from the message and format citations as footnotes."""
    message_content = message.content[0].text
    annotations = (
        message_content.annotations if hasattr(message_content, "annotations") else []
    )
    citations = []

    # Iterate over the annotations and add footnotes
    for index, annotation in enumerate(annotations):
        # Replace the text with a footnote
        message_content.value = message_content.value.replace(
            annotation.text, f" [{index + 1}]"
        )

        # Gather citations based on annotation attributes
        if file_citation := getattr(annotation, "file_citation", None):
            # This should be replaced with actual file retrieval
            citations.append(
                f"[{index + 1}] {file_citation.quote} from {file_citation.file_name}"
            )
        elif file_path := getattr(annotation, "file_path", None):
            # TODO: This should be replaced with actual file retrieval
            citations.append(
                f"[{index + 1}] Click [here](#) to download {file_path}"
            )  # The download link should be replaced with the actual download path

    # Add footnotes to the end of the message content
    full_response = message_content.value + "\n\n" + "\n".join(citations)
    return full_response


# The main interface ...
st.title("Study Buddy")
st.write("Learn fast by chatting wih your documents")

# Check sessions
if st.session_state.start_chat:
    if "openai_model" not in st.session_state:
        st.session_state.openai_model = model
        st.write("Mon modèle : " + st.session_state.openai_model)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Show exisiting messages if any...
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            print(
                f"Showing message - Role: {message['role']}, Content: {message['content']}"
            )  # Debugging output

    # chat input for user
    if prompt := st.chat_input("What's new"):
        print("Nouveau message")
        st.session_state.messages.append({"role": "user", "content": prompt})
        print(prompt)
        with st.chat_message("user"):
            st.markdown(prompt)
        print("User input:", prompt)

        # add the user's message to the existing thread
        response = client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id, role="user", content=prompt
        )
        print("Response from creating user message:", response)

        # Create and run with additionnal instructions
        run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=assis_id,
            instructions="""Please answer the questions using the knowledge provided in the files when adding additionnal information, make sure to distinguish it with bold or underlined text""",
        )
        print("Assistant run created:", run)

        # Show a spinner while the assistant is thinking
        with st.spinner("Wait... Generating response..."):
            run_completed = False
            while not run_completed:
                time.sleep(1)
                run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state.thread_id, run_id=run.id
                )
                if run.status == "completed":
                    run_completed = True
                    messages = client.beta.threads.messages.list(
                        thread_id=st.session_state.thread_id
                    )
                    print("Messages retrieved:", messages)
                    assistant_messages_for_run = [
                        message
                        for message in messages
                        if message.run_id == run.id and message.role == "assistant"
                    ]
                    print("Assistant messages for run:", assistant_messages_for_run)

                    for message in assistant_messages_for_run:
                        full_response = process_message_with_citations(message=message)
                        st.session_state.messages.append(
                            {"role": "assistant", "content": full_response}
                        )
                        with st.chat_message("assistant"):
                            st.markdown(full_response, unsafe_allow_html=True)
                        print("Assistant response:", full_response)

    else:
        # Prompt users to start chat
        st.write(
            "Please upload at least a file to get strated by clicking on the button start"
        )