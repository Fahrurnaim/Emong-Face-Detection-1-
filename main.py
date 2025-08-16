from ultralytics import YOLO
import cv2
import requests

# Load model YOLO (pastikan best.pt sesuai dengan kelas emosi)
model = YOLO("best.pt")

# Endpoint Flask API (samakan dengan api.py → /update_emotion)
API_URL = "http://127.0.0.1:5000/update_emotion"

cap = cv2.VideoCapture(0)  # buka webcam

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Prediksi YOLO dengan threshold confidence
    results = model(frame, conf=0.25)

    # Frame dengan anotasi
    annotated_frame = frame.copy()

    for r in results:
        annotated_frame = r.plot()  # hasil frame dengan box + label

        for box in r.boxes:
            cls = int(box.cls[0])              # index kelas
            conf = float(box.conf[0])          # confidence
            label = model.names[cls]           # nama kelas (emosi)

            # === Kirim hasil ke Flask ===
            payload = {"emotion": label, "confidence": conf}
            try:
                requests.post(API_URL, json=payload)
            except Exception as e:
                print(f"⚠️ Gagal update ke API: {e}")

    # Tampilkan hasil
    cv2.imshow("EMONG Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
