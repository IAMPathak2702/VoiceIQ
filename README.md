# VoiceIQ: Artificial Intelligence Interviewer

VoiceIQ is a Streamlit application that simulates an AI interviewer for a Generative AI developer position. It leverages the OpenAI API to transcribe audio recordings, generate AI responses, and convert text to speech.

## Features

- Record audio from the user using the built-in microphone.
- Transcribe the recorded audio to text using OpenAI's Whisper model.
- Generate AI responses based on the transcribed text using OpenAI's GPT-3.5-turbo model.
- Convert the AI-generated text to speech using OpenAI's TTS model.
- Play the generated audio response within the Streamlit app.
- Display the AI response and the user's transcribed text in a chat-like interface.

## Getting Started

To run the VoiceIQ application, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/IAMPathak2702/VoiceIQ.git
```

````

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Obtain an OpenAI API key by creating an account on the [OpenAI website](https://openai.com/).

4. Run the Streamlit app:

```bash
streamlit run app.py
```

5. Enter your OpenAI API key in the sidebar.

6. Click the "Mic" button and speak "MY NAME IS {YOUR NAME}" to test your microphone and start the interview.

7. The app will transcribe your audio, generate an AI response, and play the generated audio response.

## Approach and Libraries

The VoiceIQ application uses the following libraries:

- **Streamlit**: A Python library for building interactive web applications.
- **OpenAI**: The official Python library for the OpenAI API, used for transcription, text generation, and text-to-speech conversion.
- **streamlit-webrtc**: A Streamlit component for capturing audio and video streams using WebRTC.
- **audio-recorder-streamlit**: A Streamlit component for recording audio from the user's microphone.
- **av**: A library for audio/video processing used by the streamlit-webrtc component.
- **base64**: A standard Python library for encoding and decoding binary data.

The application follows these steps:

1. Set up the Streamlit app and user interface.
2. Obtain the OpenAI API key from the user.
3. Use the `audio_recorder` component to record audio from the user's microphone.
4. Save the recorded audio to a file.
5. Transcribe the recorded audio using OpenAI's Whisper model with the `transcribe_audio` function.
6. Generate an AI response based on the transcribed text using OpenAI's GPT-3.5-turbo model with the `fetch_ai_response` function.
7. Convert the AI-generated text to speech using OpenAI's TTS model with the `text_to_speech` function.
8. Play the generated audio response in the Streamlit app using HTML and JavaScript.
9. Display the AI response and the user's transcribed text in a chat-like interface using Streamlit's `st.chat_message`.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the [GitHub repository](https://github.com/IAMPathak2702/VoiceIQ).

## License

This project is licensed under the [MIT License](LICENSE).

````
