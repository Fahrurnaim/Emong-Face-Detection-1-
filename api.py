from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Data emosi terakhir
latest_emotion = {"emotion": "neutral", "confidence": 0.0}


@app.route("/")
def index():
    # Pastikan kamu punya file templates/index.html
    try:
        return render_template("index.html")
    except:
        return jsonify({"message": "Frontend belum tersedia, tapi API berjalan"})


@app.route("/update_emotion", methods=["POST"])
def update_emotion():
    """Endpoint untuk menerima update emosi dari main.py"""
    global latest_emotion
    data = request.get_json()

    if not data or "emotion" not in data or "confidence" not in data:
        return {"status": "error", "message": "Invalid data"}, 400

    latest_emotion = data
    return {"status": "ok"}


def background_emotion_sender():
    """Task untuk broadcast emosi terbaru ke semua client"""
    while True:
        socketio.emit("emotion_update", latest_emotion)
        socketio.sleep(1)  # pakai socketio.sleep agar tidak blokir event loop


@socketio.on("connect")
def handle_connect():
    print("Client connected")
    # langsung kirim data saat user connect
    socketio.emit("emotion_update", latest_emotion)


if __name__ == "__main__":
    # Jalankan background task saat server mulai
    socketio.start_background_task(background_emotion_sender)
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
