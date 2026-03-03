import cv2
import serial
import time
from ultralytics import YOLO

# 1. Initialize Serial Port (Check your Arduino IDE for the correct COM port)
arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)
time.sleep(2) # Wait for connection to stabilize

# 2. Load your custom YOLOv8 model trained for discoloration
model = YOLO('discoloration_model.pt') 

cap = cv2.VideoCapture(0) # 0 for default webcam

while cap.isOpened():
    success, frame = cap.read()
    if success:
        results = model(frame, conf=0.5) # Detect objects
        
        discoloration_found = False
        for result in results:
            # Check if any detected box belongs to your 'discoloration' class
            # Assuming 'discoloration' is class index 0
            if 0 in result.boxes.cls:
                discoloration_found = True
        
        if discoloration_found:
            arduino.write(b'1') # Send '1' to Arduino to trigger action
            print("Discoloration Detected!")
        else:
            arduino.write(b'0') # Send '0' to stop action
            
        # Display the feed
        annotated_frame = results[0].plot()
        cv2.imshow("YOLOv8 Detection", annotated_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()