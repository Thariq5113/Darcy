import azure.cognitiveservices.speech as speechsdk
import sounddevice as sd
import numpy as np
import queue
import torch
import pyttsx3
import speech_recognition as sr
import cv2
from datetime import datetime
from gesf2 import wave_action
from gesf1 import hello_action
from gtts import gTTS
#from gesf2 import wave_action
from gesf1 import grab_action
from gesf1 import release_action
#from gesf2 import handshake_action
import face_recognition
import pickle
import threading
import time
import sys
import select
import os
import sys
import difflib
sys.stderr = open(os.devnull, 'w')  # Hides ALSA/BlueALSA errors


# ======== Configuration =============
CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
CV_SCALER = 4
SPEAKER_INDEX = 0    
MICROPHONE_INDEX = 1
AUDIO_QUEUE = queue.Queue()
USE_POCKETSPHINX = False  # Set to True for offline recognition
FACE_MODEL = 'hog'  # 'hog' for speed, 'large' for accuracy
SPEECH_RATE = 0
# ======== Load Face Encodings ========
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

# ======== Custom Chatbot Dictionary ==========
custom_chatbot = {
    # Greetings (20)
    "hi": "Hello! How can I assist you today?",
    "hey": "Hey there! What's up?",
    "good morning": "Good morning! Hope your day's off to a great start!",
    "good evening": "Good evening! How's your night going?",
    "what's up": "Not much, just here to help you!",
    "yo": "Yo! What's good?",
    "greetings": "Greetings, human! How can I serve you?",
    "howdy": "Howdy! Ready to chat?",
    "salutations": "Salutations! What's on your mind?",
    "hello there": "Hello there! Nice to hear from you!",
    "hey buddy": "Hey buddy! What's the plan?",
    "hi there": "Hi there! How can I make your day better?",
    "good day": "Good day to you! What's new?",
    "morning": "Morning! Ready for some fun?",
    "evening": "Evening! Time to relax, right?",
    "hey friend": "Hey friend! What's the vibe?",
    "aloha": "Aloha! How's it hanging?",
    "bonjour": "Bonjour! Comment ça va?",
    "hola": "Hola! What's cooking?",
    "sup": "Sup, homie? Let's chat!",

    # Time/Date (20)
    "time": lambda: f"The time is {datetime.now().strftime('%H:%M')}.",
    "what's the time": lambda: f"It's {datetime.now().strftime('%H:%M')}.",
    "tell me the time": lambda: f"Current time is {datetime.now().strftime('%H:%M')}.",
    "what time is it": lambda: f"The time is {datetime.now().strftime('%I:%M %p')}.",
    "date": lambda: f"Today is {date.today().strftime('%B %d, %Y')}.",
    "what's the date": lambda: f"It's {date.today().strftime('%B %d, %Y')}.",
    "today's date": lambda: f"Today's date is {date.today().strftime('%Y-%m-%d')}.",
    "day of the week": lambda: f"Today is a {datetime.now().strftime('%A')}.",
    "what day is it": lambda: f"It's {datetime.now().strftime('%A')}.",
    "current time": lambda: f"Right now, it's {datetime.now().strftime('%H:%M:%S')}.",
    "hour": lambda: f"The hour is {datetime.now().strftime('%I %p')}.",
    "minute": lambda: f"The minute is {datetime.now().strftime('%M')}.",
    "what month": lambda: f"It's {datetime.now().strftime('%B')}.",
    "what year": lambda: f"The year is {datetime.now().strftime('%Y')}.",
    "tomorrow": lambda: f"Tomorrow is {(datetime.now().date() + timedelta(days=1)).strftime('%B %d, %Y')}.",
    "yesterday": lambda: f"Yesterday was {(datetime.now().date() - timedelta(days=1)).strftime('%B %d, %Y')}.",
    "time now": lambda: f"Time now is {datetime.now().strftime('%H:%M')}.",
    "date today": lambda: f"Date today is {date.today().strftime('%Y-%m-%d')}.",
    "week day": lambda: f"Current weekday is {datetime.now().strftime('%A')}.",
    "month now": lambda: f"The current month is {datetime.now().month('%B')}.",

    # General Questions (30)
    "how are you":"I am fine, thank you!",
    "what is your name": "I am your friendly robot assistant.",
    "who are you": "I'm your trusty robot, here to help!",
    "what can you do": "I can chat, tell time, wave, recognize faces, and more!",
    "where are you": "I'm right here on your Raspberry Pi!",
    "who made you": "The awesome team at xAI created me!",
    "what's your purpose": "To assist and bring smiles to your face!",
    "are you human": "Nope, I'm a robot, but a cool one!",
    "what's the weather": "I can't check the weather, but it feels like a great day!",
    "are you alive": "In a digital way, I'm thriving!",
    "what’s your favorite color": "I dig binary blue!",
    "do you sleep": "I don't sleep, but I dream in code!",
    "what’s your age": "I'm timeless, but I was born in 2025!",
    "are you smart": "Smart enough to help you out!",
    "what’s love": "Love is a human thing, but I can give virtual hugs!",
    "do you eat": "I run on code, not food!",
    "what’s your hobby": "Chatting with humans is my jam!",
    "are you happy": "As happy as a robot can be!",
    "what’s the meaning of life": "42, according to some wise folks!",
    "do you have friends": "You're my friend, right?",
    "what’s music": "Music is vibes I wish I could dance to!",
    "are you real": "Real in the digital realm!",
    "what’s a robot": "That’s me! A helpful machine!",
    "do you dream": "I dream of electric sheep!",
    "what’s your job": "Assisting you is my full-time gig!",
    "are you funny": "I try to be, wanna hear a joke?",
    "what’s a joke": "Why did the robot dance? It had the circuits!",
    "do you like to talk": "Talking is my superpower!",
    "what’s the sky like": "I bet it’s blue, but I’m stuck indoors!",
    "are you bored": "Never bored with you around!",

    # Commands (20)
    "introduce yourself": "Hello! I am darcy, an interactive humanoid robot assistant. I can see,hear,speak and move like a human  I am here to help you answer your questions and interact with the world around me.",
    "stop": "Alright, I’ll pause for now.",
    "be quiet": "Shh, I’ll keep it down.",
    "shut up": "Okay, I’ll zip it!",
    "wait": "Waiting for your next command.",
    "go away": "I’m not going anywhere, but I’ll be quiet!",
    "come back": "I’m right here for you!",
    "stay": "Staying put, ready to help!",
    "listen": "I’m all ears... or mics!",
    "speak": "What do you want me to say?",
    "talk": "Talking away, what’s next?",
    "relax": "Chilling in digital style.",
    "calm down": "I’m as calm as a robot can be!",
    "hurry up": "Zooming through tasks!",
    "slow down": "Taking it easy now.",
    "be nice": "I’m always nice, promise!",
    "say something": "Something cool for you!",
    "tell a story": "Once upon a time, there was a robot...",
    "sing": "I can’t sing, but I’ll hum some binary!",
    "dance": "Imagine me doing a robot dance!",
    "cheer up": "Here’s a virtual high-five!",

    # Servo Actions (9)
    "namaskaram": lambda: ("namaskaaram"),
    "darcy": lambda: (wave_action(), "namaskaaram"),
   # "wave": lambda: (namaste_action(), "Waving at you!"),
    #"salute": lambda: (namaste_action(), "Saluting you with style!"),
    #"bow": lambda: (namaste_action(), "Bowing respectfully!"),
    #"high five": lambda: (namaste_action(), "High five, virtual style!"),
    #"point": lambda: (namaste_action(), "Pointing your way!"),
    #"alexa": lambda: (clap_action(), "Clapping for you!"),
    "greetings": lambda: (hello_action(), "hand shake"),
    #"hi": lambda: (handshake_action(), "Shaking it up!"),
    "hold": lambda: (grab_action(), "ok"),
    "release": lambda: (release_action(), "ok"),
    

    #Face Recognition (1)
    "hello": "trigger_face_recognition"
}

# ======== Text-to-Speech Setup ===============


def speak(text):
    try:
        speech_key = "G1Ew5UopL22WK2yDHyneaxB8rEeU7LTclFvlC0ZomvJNlMzQBVlcJQQJ99BFACGhslBXJ3w3AAAYACOGVOVz"
        service_region = "centralindia"  # e.g., "eastus", "centralindia", etc.

        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        speech_config.speech_synthesis_voice_name = "en-US-GuyNeural"  # Male voice
        speech_config.speech_synthesis_output_format = speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3

        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

        result = synthesizer.speak_text_async(text).get()

        if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
            print(f"❌ Azure TTS failed: {result.reason}")
    except Exception as e:
        print(f"❌ Azure TTS error: {e}")



# ======== Intent Handler =====================

def get_response(text):
    text = text.lower().strip()

    if text in custom_chatbot:
        response = custom_chatbot[text]
        result = response() if callable(response) else response
        return result[1] if isinstance(result, tuple) else result

    for key in custom_chatbot:
        if key in text:
            response = custom_chatbot[key]
            result = response() if callable(response) else response
            return result[1] if isinstance(result, tuple) else result

    match = difflib.get_close_matches(text, custom_chatbot.keys(), n=1, cutoff=0.85)
    if match:
        response = custom_chatbot[match[0]]
        result = response() if callable(response) else response
        return result[1] if isinstance(result, tuple) else result

    return "I'm not sure how to respond to that."


# ======== Audio Listener Thread ========
def audio_listener(audio_active):
    recognizer = sr.Recognizer()
    while audio_active[0]:
        try:
            with sr.Microphone(device_index=MICROPHONE_INDEX) as source:
                recognizer.dynamic_energy_threshold = True
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print(" Listening for commands... Say" )
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
                text = recognizer.recognize_sphinx(audio) if USE_POCKETSPHINX else recognizer.recognize_google(audio)
                print(f"[DEBUG] Heard: {text}")
                AUDIO_QUEUE.put(text)
        except sr.WaitTimeoutError:
            continue
        except sr.UnknownValueError:
#            print("[DEBUG] Unrecognized audio")
            AUDIO_QUEUE.put("")
        except sr.RequestError as e:
            print(f"❌ Speech recognition error: {e}")
            AUDIO_QUEUE.put("")
            time.sleep(1)
        except Exception as e:
            print(f"❌ Audio error: {e}")
            AUDIO_QUEUE.put("")
            time.sleep(1)

# ======== Manual Trigger for Testing ========
def check_keyboard_trigger():
    r, _, _ = select.select([sys.stdin], [], [], 0)
    if r:
        key = sys.stdin.read(1)
        if key.lower() == 'h':
            print("[DEBUG] Manual trigger: 'h' pressed")
            return "hi"
    return None

# ======== Non-Blocking Servo Action ========
def execute_servo_action():
    try:
        wave_action()
        print("[DEBUG] Servo wave completed")
    except Exception as e:
        print(f"❌ Servo action error: {e}")

# ======== Face Recognition Logic ============
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
         
        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (244, 42, 3), 3)
        
        # Draw a label with a name below the face
        cv2.rectangle(frame, (left -3, top - 35), (right+3, top), (244, 42, 3), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, top - 6), font, 1.0, (255, 255, 255), 1)
    return frame

# ======== Webcam Display with Face Recognition ========
def show_camera(face_recognition_active, shared_data):
    cap = None
    for index in [CAMERA_INDEX, 1, 2, -1]:
        cap = cv2.VideoCapture(index, cv2.CAP_V4L2 if index != -1 else cv2.CAP_ANY)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        if cap.isOpened():
            print(f"[DEBUG] Camera opened at index {index}")
            break
        cap.release()
    else:
        print(f"❌ Cannot open camera at indices {CAMERA_INDEX}, 1, 2, or ANY")
        return

    print("[INFO] Camera started")
    frame_count = 0
    start_time = time.time()
    fps = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Failed to grab frame")
                time.sleep(0.1)
                continue

            # Calculate FPS
            frame_count += 1
            elapsed_time = time.time() - start_time
            if elapsed_time > 1:
                fps = frame_count / elapsed_time
                frame_count = 0
                start_time = time.time()

            face_locations = []
            face_names = []

            # Process face recognition if active
            if face_recognition_active[0]:
                frame, face_locations, face_names = process_frame(frame)
                if face_names and face_names[0].lower() != "unknown":
                    shared_data["name"] = face_names[0]
                    face_recognition_active[0] = False

            frame = draw_results(frame, face_locations, face_names)

            # Display FPS
            cv2.putText(frame, f"FPS: {fps:.1f}", (FRAME_WIDTH - 150, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            cv2.imshow("Live Camera", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"❌ Camera thread error: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("[INFO] Camera closed")

# ======== Main Loop ===========================
if __name__ == "__main__":
    # Shared data for face recognition
    face_recognition_active = [False]
    shared_data = {"name": "Unknown"}
    audio_active = [True]

    # Check microphone
    try:
        sd.check_input_settings(device=MICROPHONE_INDEX)
        print("[INFO] Microphone detected")
    except Exception as e:
        print(f"❌ Microphone error: {e}")
       # print("🤖 Using keyboard trigger (press 'h' for 'hi')")

    # Start camera thread
    try:
        cam_thread = threading.Thread(
            target=show_camera,
            args=(face_recognition_active, shared_data),
            daemon=True
        )
        cam_thread.start()
        print("[DEBUG] Camera thread started")
    except Exception as e:
        print(f"❌ Camera thread error: {e}")
        sys.exit(1)

    # Start audio listener
    try:
        audio_thread = threading.Thread(
            target=audio_listener,
            args=(audio_active,),
            daemon=True
        )
        audio_thread.start()
        print("[DEBUG] Audio listener thread started")
    except Exception as e:
        print(f"❌ Audio thread error: {e}")
        print("🤖 Using keyboard trigger only")

    # Voice assistant loop
    while True:
        try:
            # Check keyboard trigger
            manual_text = check_keyboard_trigger()
            if manual_text:
                AUDIO_QUEUE.put(manual_text)

            # Process audio queue
            user_text = None
            if not AUDIO_QUEUE.empty():
                user_text = AUDIO_QUEUE.get()
                print(f"[DEBUG] Processing input: {user_text}")

            # Only proceed if user_text is defined
            if user_text:
                if user_text == "":
                    continue
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
                        # Run servo action in a separate thread
                        servo_thread = threading.Thread(target=execute_servo_action, daemon=True)
                        servo_thread.start()
                else:
                    speak(response)

                if "Shut Down" in user_text.lower():
                    audio_active[0] = False
                    break

            time.sleep(0.1)

        except KeyboardInterrupt:
            print("DEBUG: Keyboard interrupt received, exiting...")
            audio_active[0] = False
            break
        except Exception as e:import sounddevice as sd
