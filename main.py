from ultralytics import YOLO
import cv2
import requests

model = YOLO("best.pt")

API_URL = "http://127.0.0.1:5000/update_emotion"

cap = cv2.VideoCapture(0)  

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, conf=0.25)

    annotated_frame = frame.copy()

    for r in results:
        annotated_frame = r.plot()  

        for box in r.boxes:
            cls = int(box.cls[0])             
            conf = float(box.conf[0])        
            label = model.names[cls]         

            payload = {"emotion": label, "confidence": conf}
            try:
                requests.post(API_URL, json=payload)
            except Exception as e:
                print(f"⚠️ Gagal update ke API: {e}")

    cv2.imshow("EMONG Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
