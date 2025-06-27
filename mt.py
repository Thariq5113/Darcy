import os
import cv2
import face_recognition
import pickle

# Path to dataset
DATASET_DIR = "/home/ecerobo/face_images"
ENCODINGS_FILE = "encodings.pickle"

known_encodings = []
known_names = []

print("[INFO] Processing face images...")

# Loop over each person folder
for person_name in os.listdir(DATASET_DIR):
    person_path = os.path.join(DATASET_DIR, person_name)

    if not os.path.isdir(person_path):
        continue

    print(f"[INFO] Processing {person_name}...")

    for image_name in os.listdir(person_path):
        image_path = os.path.join(person_path, image_name)

        # Load image and convert to RGB
        image = cv2.imread(image_path)
        if image is None:
            print(f"[WARNING] Unable to read {image_path}, skipping...")
            continue

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Detect face locations and encodings
        boxes = face_recognition.face_locations(rgb, model='hog')
        encodings = face_recognition.face_encodings(rgb, boxes)

        for encoding in encodings:
            known_encodings.append(encoding)
            known_names.append(person_name)

# Save encodings to pickle file
print("[INFO] Serializing encodings...")
data = {"encodings": known_encodings, "names": known_names}
with open(ENCODINGS_FILE, "wb") as f:
    pickle.dump(data, f)

print(f"[✅] Saved encodings to {ENCODINGS_FILE}")
