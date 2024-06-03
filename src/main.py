from fastapi import FastAPI, UploadFile, File
import os
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import uvicorn
from openai import OpenAI
import json

client = OpenAI()

app = FastAPI(
    title="Interview Chatbot",
    summary="Takes interview of candidates",
)


@app.get("/")
def hello_world():
    return {"messages": "hello_world"}


@app.post("/talk")
async def post_audio(file: UploadFile = File(...)):
    user_message = transcribe_audio(file)
    chat_response = get_chat_response(user_message)
    return user_message


# 1. Send in audio and have it transcribed
def transcribe_audio(file):
    audio_file= open(file.filename, "rb")
    with open(file.filename, 'wb') as buffer:
        buffer.write(file.file.read())
    audio_file = open(file.filename, "rb")
    transcript = client.audio.transcriptions.create(model="whisper-1",file=audio_file, response_format="text")
    print(transcript)
    return transcript


# 2. we want to send it to chatgpt and get a response
def get_chat_response(user_message):
    messages = load_messages()
    messages.append({"role": "user", "content": user_message})
    print(messages)
    # Send to ChatOpenAI
    gpt_response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    gpt_response_content = gpt_response.choices[0].message.content
    # Save messages
    save_messages(user_message, gpt_response_content)


def load_messages():
    messages = []
    file = "src/database.json"

    # If file is empty, add the context
    empty = os.stat(file).st_size == 0

    # If file is not empty, loop through history to add messages
    if not empty:
        try:
            with open(file) as db_file:
                data = json.load(db_file)
                for item in data:
                    messages.append(item)
        except json.JSONDecodeError:
            print("Error loading JSON data from the file. Using default context.")

    if not messages:
        messages.append(
            {
                "role": "system",
                "content": "You are interviewing the user for a Generative AI developer position. Ask short questions that are relevant to a junior level developer. Your name is GiGi. User name is Ved. Keep responses under 30 words and be funny and humorous sometimes."
            }
        )
    return messages

def save_messages(user_message, gpt_response_content):
    file = 'src/database.json'
    messages = load_messages()
    messages.append({"role": "user", "content": user_message})
    messages.append({"role": "assistant", "content": gpt_response_content})
    with open(file, 'w') as f:
        json.dump(messages, f)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)