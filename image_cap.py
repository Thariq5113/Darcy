import cv2
import os
import time
from datetime import datetime

# Create a folder for the captured images
folder_name = "captured_frames_" + datetime.now().strftime("%Y%m%d_%H%M%S")
os.makedirs(folder_name, exist_ok=True)

# Open the camera using V4L2 backend
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

# Force MJPEG format and resolution that your camera supports
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2592)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1944)

if not cap.isOpened():
    print("❌ Error: Could not open webcam.")
    exit()

print(f"📷 Webcam opened. Saving images to: {folder_name}")

frame_count = 0
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Failed to grab frame.")
            continue

        filename = os.path.join(folder_name, f"frame_{frame_count}.jpg")
        cv2.imwrite(filename, frame)
        print(f"✅ Saved: {filename}")
        frame_count += 1
        time.sleep(5)  # Wait 5 seconds between captures

except KeyboardInterrupt:
    print("\n⏹️ Stopped by user.")
finally:
    cap.release()
    print("📷 Webcam released.")


