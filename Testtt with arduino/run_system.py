import cv2
import serial
from ultralytics import YOLO
import time

# --- CONFIGURATION ---
arduino = serial.Serial('COM5', 9600, timeout=1)
time.sleep(2)  # Allow Arduino to reset
model = YOLO('best.pt')
# ---------------------

cap = cv2.VideoCapture(0)

print("System running... Press 'q' to stop.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, conf=0.5)

    discoloration_detected = False

    for box in results[0].boxes:
        cls = int(box.cls[0])
        label = results[0].names[cls].lower()

        if label == "discoloration":
            discoloration_detected = True
            break

    if discoloration_detected:
        arduino.write(b'1')
        status_text = "DISCOLORATION DETECTED"
        color = (0, 0, 255)
    else:
        arduino.write(b'0')
        status_text = "NORMAL"
        color = (0, 255, 0)

    annotated_frame = results[0].plot()
    cv2.putText(annotated_frame, status_text, (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    cv2.imshow("Detection Feed", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()