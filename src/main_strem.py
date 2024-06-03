import streamlit as st
import os
import json
import tempfile
from openai import OpenAI
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import av
import time

# Initialize the OpenAI client
client = OpenAI()
st.set_page_config(page_title="Interview Chatbot", layout="wide")
# Set up the Streamlit app
st.title("Interview Chatbot")
st.write("This chatbot will take your interview for a Generative AI developer position.")

# Function to transcribe audio
def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file, response_format="text")
    if isinstance(transcript, str):
        return transcript
    else:
        return transcript.get('text', "Error transcribing audio.")

# Function to get chat response from ChatGPT
def get_chat_response(user_message):
    messages = load_messages()
    messages.append({"role": "user", "content": user_message})
    gpt_response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    gpt_response_content = gpt_response.choices[0].message.content
    save_messages(user_message, gpt_response_content)
    return gpt_response_content

# Function to load chat history
def load_messages():
    messages = []
    file = "database.json"
    if os.path.exists(file) and os.stat(file).st_size != 0:
        try:
            with open(file) as db_file:
                data = json.load(db_file)
                messages.extend(data)
        except json.JSONDecodeError:
            st.error("Error loading JSON data from the file. Using default context.")
    
    if not messages:
        messages.append({
            "role": "system",
            "content": "You are interviewing the user for a Generative AI developer position. Ask short questions that are relevant to a junior level developer. Your name is GiGi. User name is Ved. Keep responses under 30 words and be funny and humorous sometimes."
        })
    
    return messages

# Function to save chat history
def save_messages(user_message, gpt_response_content):
    file = 'database.json'
    messages = load_messages()
    messages.append({"role": "user", "content": user_message})
    messages.append({"role": "assistant", "content": gpt_response_content})
    with open(file, 'w') as f:
        json.dump(messages, f)

# Recorder class to capture audio stream
class AudioProcessor:
    def __init__(self):
        self.frames = []

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        self.frames.append(frame)
        return frame

# WebRTC settings
webrtc_ctx = webrtc_streamer(
    key="audio_recorder",
    mode=WebRtcMode.SENDONLY,
    client_settings=ClientSettings(
        media_stream_constraints={"audio": True, "video": False}
    ),
    audio_processor_factory=AudioProcessor
)

if 'recording' not in st.session_state:
    st.session_state['recording'] = False
    start_time = 0  # Initialize start_time to 0

# Divide the screen into two columns
left_column, right_column = st.columns(2)

# Left column: Display user and AI responses
with left_column:
    chat_container = st.container()
    with chat_container:
        messages = load_messages()
        for message in messages:
            if message['role'] == 'user':
                st.write(f"<div style='text-align: right; color: blue;'>{message['role'].capitalize()}: {message['content']}</div>", unsafe_allow_html=True)
            else:
                st.write(f"<div style='text-align: left; color: green;'>{message['role'].capitalize()}: {message['content']}</div>", unsafe_allow_html=True)

        # Scroll to the bottom of the chat container
        chat_container.write("")
        chat_container.markdown("""
            <script>
                var container = window.parent.document.querySelector('div[data-testid="stAppViewContainer"] > div:last-child');
                container.scrollIntoView({ behavior: 'smooth', block: 'end' });
            </script>
        """, unsafe_allow_html=True)

# Right column: Chat input field and recording buttons
with right_column:
    chat_input = st.text_input("Enter your message or click the 'Start Recording' button:", key="chat_input")

    # Start Recording button
    start_recording = st.button("Start Recording")

    # Get Single Response button
    get_single_response = st.button("Get Single Response")

    if start_recording or webrtc_ctx.state.playing:
        if start_recording:
            start_time = time.time()  # Assign start_time when recording starts
            st.session_state['recording'] = True
            # Append system message from assistant
            save_messages("", "Hey again, Ved! Let's get this interview party started. Tell me, what sparked your interest in Generative AI development? Or was it just the thrill of creating code that outsmarts you sometimes?")

        if webrtc_ctx.state.playing:
            st.info("Recording...")

            elapsed_time = time.time() - start_time
            if elapsed_time >= 10 or st.button("Stop Recording"):
                audio_processor = webrtc_ctx.audio_processor
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
                    audio_data = b"".join([frame.to_ndarray().tobytes() for frame in audio_processor.frames])
                    tmpfile.write(audio_data)
                    tmpfile_path = tmpfile.name

                st.write("Transcribing audio...")
                transcript = transcribe_audio(tmpfile_path)
                st.write("Transcription:", transcript)

                # Get chat response
                chat_response = get_chat_response(transcript)

                # Clean up temporary file
                os.remove(tmpfile_path)
                st.session_state['recording'] = False
            else:
                remaining_time = 10 - int(elapsed_time)
                st.write(f"Recording will stop in {remaining_time} seconds...")

        else:
            if chat_input:
                chat_response = get_chat_response(chat_input)

    elif get_single_response:
        if chat_input:
            chat_response = get_chat_response(chat_input)
            st.write(f"<div style='text-align: left; color: green;'>Assistant: {chat_response}</div>", unsafe_allow_html=True)