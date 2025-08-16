// Connect ke server Flask via WebSocket
const socket = io("http://127.0.0.1:5000");

// Terima data emosi dari server
socket.on("emotion_update", (data) => {
  document.getElementById("emotion-box").innerText =
    `Emotion: ${data.emotion} | Confidence: ${Math.round(data.confidence * 100)}%`;
});
