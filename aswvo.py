import os
import queue
import threading
import time
import sys
import select
import json
import cv2
import face_recognition
import pickle
import numpy as np
from datetime import datetime, date, timedelta
from sounddevice import RawInputStream, query_devices
from vosk import Model, KaldiRecognizer
import difflib
import soundfile as sf
import sounddevice as sd

from gesf2 import wave_action
from gesf1 import hello_action, grab_action, release_action

CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
CV_SCALER = 4
SPEAKER_INDEX = 0
MICROPHONE_INDEX = 1
AUDIO_QUEUE = queue.Queue()
FACE_MODEL = 'hog'
SPEECH_RATE = 130

print("[INFO] Loading Vosk model...")
vosk_model = Model("/home/ecerobo/models/vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(vosk_model, 48000)

print("[INFO] Loading encodings...")
try:
    with open("/home/ecerobo/encodings.pickle", "rb") as f:
        data = pickle.load(f)
    known_face_encodings = data["encodings"]
    known_face_names = data["names"]
    print(f"[DEBUG] Loaded {len(known_face_names)} encodings")
except Exception as e:
    print(f"❌ Error loading encodings.pickle: {e}")
    sys.exit(1)

custom_chatbot = {
    "hi": "Hello! How can I assist you today?",
    "hello": "trigger_face_recognition",
    "grab": lambda: (grab_action(), "ok"),
    "release": lambda: (release_action(), "ok"),
    "darcy": lambda: (wave_action(), "hi there, nice to meet you"),
    "greetings": lambda: (hello_action(), "hand shake"),
}

def speak(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', SPEECH_RATE)
        engine.save_to_file(text, 'temp.wav')
        engine.runAndWait()
        data, fs = sf.read('temp.wav')
        sd.play(data, fs, device=SPEAKER_INDEX)
        sd.wait()
    except Exception as e:
        print(f"❌ TTS error: {e}")

def get_response(text):
    text = text.lower().strip()
    if text in custom_chatbot:
        response = custom_chatbot[text]
        return response() if callable(response) else response
    for key in custom_chatbot:
        if key in text:
            response = custom_chatbot[key]
            return response() if callable(response) else response
    match = difflib.get_close_matches(text, custom_chatbot.keys(), n=1, cutoff=0.85)
    if match:
        response = custom_chatbot[match[0]]
        return response() if callable(response) else response
    return "I'm not sure how to respond to that."

def vosk_listener(audio_active):
    def callback(indata, frames, time, status):
        if recognizer.AcceptWaveform(indata):
            result = json.loads(recognizer.Result())
            if "text" in result:
                AUDIO_QUEUE.put(result["text"])
    with RawInputStream(samplerate=48000, blocksize=8000, dtype='int16', channels=1, callback=callback, device=MICROPHONE_INDEX):
        print("[INFO] Listening (Vosk)...")
        while audio_active[0]:
            time.sleep(0.1)

def process_frame(frame):
    print("[DEBUG] Processing frame for face recognition")
    try:
        resized_frame = cv2.resize(frame, (0, 0), fx=(1/CV_SCALER), fy=(1/CV_SCALER))
        rgb_resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_resized_frame, model=FACE_MODEL)
        face_encodings = face_recognition.face_encodings(rgb_resized_frame, face_locations)
        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            if face_distances.size > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
            face_names.append(name)
        print(f"[DEBUG] Detected {len(face_locations)} faces, names: {face_names}")
        return frame, face_locations, face_names
    except Exception as e:
        print(f"❌ Face recognition error: {e}")
        return frame, [], []

def draw_results(frame, face_locations, face_names):
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= CV_SCALER
        right *= CV_SCALER
        bottom *= CV_SCALER
        left *= CV_SCALER
        cv2.rectangle(frame, (left, top), (right, bottom), (244, 42, 3), 3)
        cv2.rectangle(frame, (left -3, top - 35), (right+3, top), (244, 42, 3), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, top - 6), font, 1.0, (255, 255, 255), 1)
    return frame

def show_camera(face_recognition_active, shared_data):
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("❌ Cannot open camera")
        return
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to grab frame")
            break
        display_frame = frame.copy()
        face_locations, face_names = [], []
        if face_recognition_active[0]:
            frame, face_locations, face_names = process_frame(frame)
            if face_names and face_names[0].lower() != "unknown":
                shared_data["name"] = face_names[0]
                face_recognition_active[0] = False
        frame = draw_results(frame, face_locations, face_names)
        cv2.imshow("Live Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def execute_servo_action():
    try:
        wave_action()
        print("[DEBUG] Servo wave completed")
    except Exception as e:
        print(f"❌ Servo action error: {e}")

if __name__ == "__main__":
    face_recognition_active = [False]
    shared_data = {"name": "Unknown"}
    audio_active = [True]

    threading.Thread(target=show_camera, args=(face_recognition_active, shared_data), daemon=True).start()
    threading.Thread(target=vosk_listener, args=(audio_active,), daemon=True).start()

    print("[INFO] Ready for commands (say 'hi' to initiate)...")
    while True:
        try:
            if not AUDIO_QUEUE.empty():
                user_text = AUDIO_QUEUE.get().strip()
                if user_text:
                    print(f"[DEBUG] Heard: {user_text}")
                    response = get_response(user_text)
                    if response == "trigger_face_recognition":
                        face_recognition_active[0] = True
                        start_time = time.time()
                        while face_recognition_active[0] and time.time() - start_time < 10:
                            time.sleep(0.5)
                        name = shared_data["name"]
                        time.sleep(0.5)
                        speak(f"Hi, {name}!")
                        if name.lower() != "unknown":
                            threading.Thread(target=execute_servo_action, daemon=True).start()
                    else:
                        speak(response)
            time.sleep(0.1)
        except KeyboardInterrupt:
            audio_active[0] = False
            break
