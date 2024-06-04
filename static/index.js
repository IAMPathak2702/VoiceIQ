let mediaRecorder;
let chunks = [];
let isRecording = false;

const recordBtn = document.getElementById("recordBtn");
const transcriptionArea = document.getElementById("transcription");
const audioPlayer = document.getElementById("audioPlayer");

recordBtn.addEventListener("click", () => {
  if (!isRecording) {
    startRecording();
    recordBtn.classList.remove("btn-primary");
    recordBtn.classList.add("btn-danger");
  } else {
    stopRecording();
    recordBtn.classList.remove("btn-danger");
    recordBtn.classList.add("btn-primary");
  }
});

async function startRecording() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream, { mimeType: "audio/mpeg" });
    mediaRecorder.start();
    isRecording = true;

    mediaRecorder.ondataavailable = (event) => {
      chunks.push(event.data);
    };
  } catch (error) {
    console.error("Error accessing audio stream:", error);
  }
}

async function stopRecording() {
  mediaRecorder.stop();
  isRecording = false;

  const blob = new Blob(chunks, { type: "audio/mpeg" });
  const filename = `recording_${Date.now()}.mp3`;
  const filepath = `C:\\Users\\vpved\\Documents\\GitHub\\VoiceIQ\\Recordings\\${filename}`;

  try {
    // Save the audio file
    await saveFile(blob, filepath);
    console.log("Audio file saved:", filepath);

    // Send the audio file to the server for transcription
    const formData = new FormData();
    formData.append("audio", blob, filename);
    const response = await fetch("http://127.0.0.1/talk", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const transcription = await response.text();
      transcriptionArea.value = transcription;

      // Play the recorded audio
      const audioUrl = URL.createObjectURL(blob);
      audioPlayer.src = audioUrl;
      audioPlayer.play();
    } else {
      console.error("Error transcribing audio:", response.statusText);
    }
  } catch (error) {
    console.error("Error sending audio to server:", error);
  }

  chunks = [];
}
// tem
async function saveFile(blob, filepath) {
  try {
    const fs = require("fs");
    const buffer = Buffer.from(await blob.arrayBuffer());
    fs.writeFileSync(filepath, buffer);
  } catch (error) {
    console.error("Error saving file:", error);
    throw error;
  }
}
