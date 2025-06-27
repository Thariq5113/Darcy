import cv2
import os
from datetime import datetime

# ======== Configuration =============
SAVE_FOLDER = "/home/ecerobo/face_images"  # Updated save location
CAMERA_INDEX = 0  # Default camera index (try 1 or 2 if 0 fails)
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# ======== Create Save Folder ========
def ensure_save_folder(folder):
    if not os.path.exists(folder):
        try:
            os.makedirs(folder)
            print(f"Created folder: {folder}")
        except Exception as e:
            print(f"❌ Error creating folder {folder}: {e}")
            return False
    return True

# ======== Generate Timestamped Filename ========
def get_timestamped_filename(name="image"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{name}_{timestamp}.jpg"

# ======== Capture and Save Image ========
def capture_photos(name="image"):
    # Ensure save folder exists
    person_folder = os.path.join(SAVE_FOLDER, name)
    if not ensure_save_folder(person_folder):
        return

    # Initialize camera
    cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_V4L2)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

    if not cap.isOpened():
        print(f"❌ Cannot open camera at index {CAMERA_INDEX}")
        return

    print(f"📷 Camera started for {name}. Press 's' to save a picture, 'q' to quit.")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Failed to grab frame")
                break

            # Display live feed
            cv2.imshow("Camera Feed", frame)

            # Check for key press
            key = cv2.waitKey(10) & 0xFF  # Increased delay for reliable input
            if key == ord('s'):
                # Save image with timestamp
                filename = get_timestamped_filename(name)
                save_path = os.path.join(person_folder, filename)
                try:
                    cv2.imwrite(save_path, frame)
                    print(f"✅ Saved image to {save_path}")
                except Exception as e:
                    print(f"❌ Error saving image to {save_path}: {e}")

            elif key == ord('q'):
                print("DEBUG: Quitting camera feed")
                break

    except KeyboardInterrupt:
        print("DEBUG: Keyboard interrupt received, exiting...")

    except Exception as e:
        print(f"❌ Camera error: {e}")

    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("📷 Camera closed")

# ======== Main Execution ========
if __name__ == "__main__":
    print("DEBUG: Starting image capture script...")
    PERSON_NAME = "Harsha Vardhini "  # Change this to the name of the person being photographed
    capture_photos(PERSON_NAME)
