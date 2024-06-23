import streamlit as st
import os
import json
import tempfile
from openai import OpenAI
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import av
import time
from audio_recorder_streamlit import audio_recorder
import base64



# Function to set up the OpenAI client
def setup_openai_client(apikey):
    """
    Set up the OpenAI client with the provided API key.

    Args:
        apikey (str): The OpenAI API key.

    Returns:
        OpenAI: The initialized OpenAI client.
    """
    return OpenAI(api_key=apikey)

# Function to transcribe audio to text

def transcribe_audio(file_path, client):
    """
    Transcribe an audio file to text using the OpenAI Whisper model.

    Args:
        file_path (str): The path to the audio file.
        client (OpenAI): The OpenAI client instance.

    Returns:
        str: The transcribed text from the audio file.
    """
    audio_file = open(file_path, "rb")
    transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file, response_format="text")
    print(transcript)
    return transcript





# Function to fetch AI response for a given input text
def fetch_ai_response(client, user_message):
    """
    Fetch an AI response from the OpenAI GPT-3.5-turbo model.

    Args:
        client (OpenAI): The OpenAI client instance.
        input_text (str): The input text for which to generate a response.

    Returns:
        str: The AI-generated response.
    """

    messages = [
        {
            "role": "system",
            "content": """You are conducting a job interview for a Junior Generative AI Developer role.
            Start with an easy question relevant to a junior level, check if the response
            is satisfactory, and provide feedback. Gradually increase the difficulty with
            each subsequent question. Keep your responses concise (under 30 words) and occasionally 
            inject some humor.""",
        },
        
        {
            "role": "user",
            "content": user_message
        }
    ]
    gpt_response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    gpt_response_content = gpt_response.choices[0].message.content
    messages.append({"role": "assistant", "content": gpt_response_content})
    return gpt_response_content


# Function to convert text to speech
def text_to_speech(text_input, audio_path, client):
    """
    Convert text to speech using the OpenAI TTS model.

    Args:
        text_input (str): The input text to convert to speech.
        audio_path (str): The path to save the generated audio file.
        client (OpenAI, optional): The OpenAI client instance. Defaults to client.

    Returns:
        None
    """
    ouput_audio = client.audio.speech.create(model="tts-1", voice="nova", input=text_input)
    ouput_audio.stream_to_file(audio_path)


import base64

def autoplay_audio(audio_file):
    """
    Automatically plays an audio file in Streamlit.

    Args:
        audio_file (str or Path): The path to the audio file.
    """
    with open(audio_file, "rb") as audio_file:
        audio_bytes = audio_file.read()

    base64_audio = base64.b64encode(audio_bytes).decode("utf-8")
    audio_html = f"""
        <audio autoplay >
            <source src="data:audio/mp3;base64,{base64_audio}" type="audio/mp3">
        </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)
        


# Main function
def main():
    """
    The main function that sets up the Streamlit app and handles the AI interviewer functionality.
    """
     # Set up the Streamlit app
    st.set_page_config(page_title="Interview Chatbot", layout="wide")
    st.markdown("""
    <h1 style="text-align: center;"> 🧠 Artificial Intelligence Interviewer 🤖</h1>
    <h4 style="text-align: center;color:red;">This chatbot will take your interview for a Generative AI developer position.</h4>
    <h6 style="text-align: center;color:green;">Click on Mic button and speak <strong style="color:yellow;"> "Greet AI with Hello" </strong> to test Your Microphone and start the interview</h6>
    """, unsafe_allow_html=True)

    # Get the OpenAI API key from the user
    api_key = st.sidebar.text_input(label="Enter your OpenAI Key", type="password")
    
    st.sidebar.info("After Inserting OPENAI API KEY , Close this sidebar",icon="⏮️")
    st.sidebar.markdown(""" ## ⚠️ Model Access Requirements

The following model access is required:

- **gpt-3.5-turbo**
- **whisper-1**
- **tts-1**
""")
    
    st.sidebar.info("Ved Prakash Pathak",icon="😄")

    if api_key:

        client = setup_openai_client(apikey=api_key)

        l1, l2, l3, l4, l5,l6,l7 = st.columns(7)
        with l4:
            # Record audio from the user
            recorded_audio = audio_recorder(text="            ",icon_size="7x")

        if recorded_audio:
            # Save the recorded audio to a file
            audio_file = "audio.MP3"
            with open(audio_file, "wb") as f:
                f.write(recorded_audio)

            # Transcribe the recorded audio to text
            transcribe_text = transcribe_audio(client=client, file_path="audio.MP3")

            # Fetch the AI response based on the transcribed text
            ai_response = fetch_ai_response(user_message=transcribe_text, client=client)
            response_audio_file = "ai_audio.MP3"
            
            
            text_to_speech(text_input=ai_response, audio_path=response_audio_file,client=client)
            
            st.audio(data=response_audio_file,format="audio/MP3")
            autoplay_audio(response_audio_file)
            st.markdown(
        """
        <script>
            const audioElement = window.parent.document.querySelector('audio');
            audioElement.play();
        </script>
        """,
        unsafe_allow_html=True
    )

            # Display the AI response and the user's transcribed text
            with st.chat_message("ai"):
                st.markdown(ai_response)
            with st.chat_message("user"):
                st.markdown(transcribe_text)

if __name__ == "__main__":
    main()