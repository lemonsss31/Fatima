# revised_yolo.py
from ultralytics import YOLO
import cv2
import time
import os

status_file = "status.txt"

def main():
    model_path = r"C:\Users\acer nitro v15\Documents\VS\PYTHON\Fatimas Thesis\tyghijerfytguhi-20260302T122919Z-1-001\tyghijerfytguhi\runs\detect\train\weights\best.pt"
    
    if not os.path.exists(model_path):
        print("❌ Model file not found at:", model_path)
        return

    print(f"✅ Found model at: {model_path}")

    model = YOLO(model_path)

    print("🚀 Running on CPU")

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("❌ Cannot open webcam")
        return

    prev_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize frame for speed
        frame = cv2.resize(frame, (640, 480))

        # Run YOLOv8 detection
        results = model(frame, imgsz=640, conf=0.5)

        # ✅ Initialize status for this frame
        discoloration_detected = False

        # Draw boxes
        for box in results[0].boxes:
            x1, y1, x2, y2 = box.xyxy[0].int().tolist()
            cls = int(box.cls[0])
            label = results[0].names[cls]
            conf = float(box.conf[0])

            if label.lower() == "discoloration":
                discoloration_detected = True

            # Draw rectangle and label
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # ✅ Write status once per frame
        with open(status_file, "w") as f:
            f.write("true" if discoloration_detected else "false")

        # FPS Counter
        current_time = time.time()
        fps = 1 / (current_time - prev_time) if prev_time != 0 else 0
        prev_time = current_time

        cv2.putText(frame, f"FPS: {int(fps)}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        # Show frame
        cv2.imshow("YOLOv8 Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()