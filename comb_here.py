from flask import Flask, render_template_string, request, redirect
import threading, time, os, pickle, face_recognition, cv2
from datetime import datetime, timedelta, date
import azure.cognitiveservices.speech as speechsdk
import difflib, sys, queue, sounddevice as sd, speech_recognition as sr
from s import grab_action, release_action, punch_action, rose_action, shake_hand_action, salute_action
import cohere

cohere_client = cohere.Client("")  # Replace with your real key

sys.stderr = open(os.devnull, 'w')

app = Flask(__name__)
AUDIO_QUEUE = queue.Queue()
MICROPHONE_INDEX = 1
FACE_MODEL = 'hog'
CV_SCALER = 4
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
CAMERA_INDEX = 0
face_recognition_active = [False]
shared_data = {"name": "Unknown"}
audio_active = [True]
speak_lock = threading.Lock()  # ✅ Lock for TTS

# ========== Load Encodings ===========
print("[INFO] Loading encodings...")
with open("/home/ecerobo/encodings.pickle", "rb") as f:
    data = pickle.load(f)
known_face_encodings = data["encodings"]
known_face_names = data["names"]
print(f"[DEBUG] Loaded {len(known_face_names)} encodings")

# ========== Custom Chatbot ===========
custom_chatbot = {
    # Greetings and time...
    "month now": lambda: f"The current month is {datetime.now().strftime('%B')}.",

    # Commands and gestures
    "nice to meet you": lambda: (shake_hand_action(), "Nice to meet you too"),
    "darcy": lambda: (salute_action(), "Namaskaaram"),
    "greetings": lambda: (rose_action(), "Welcome to Dark"),
    "grab": lambda: (grab_action(), "Got it!"),
    "release": lambda: (release_action(), "Released."),
    "beat me": lambda: (punch_action(), "That's easy."),
    "hello": "trigger_face_recognition"
}

# ========== Azure TTS ===========
def speak(text):
    with speak_lock:  # ✅ Prevent multiple simultaneous TTS
        try:
            print(f"[SPEAK] Speaking: {text}")
            speech_key = "G1Ew5UopL22WK2yDHyneaxB8rEeU7LTclFvlC0ZomvJNlMzQBVlcJQQJ99BFACGhslBXJ3w3AAAYACOGVOVz"
            service_region = "centralindia"
            speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
            speech_config.speech_synthesis_voice_name = "en-US-GuyNeural"
            speech_config.speech_synthesis_output_format = speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3
            audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
            synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
            result = synthesizer.speak_text_async(text).get()
            if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
                print(f"❌ Azure TTS failed: {result.reason}")
        except Exception as e:
            print(f"❌ Azure TTS error: {e}")

# ========== Intent Handler ===========
def get_response(text):
    text = text.lower().strip()
    if text in custom_chatbot:
        r = custom_chatbot[text]
        res = r() if callable(r) else r
        return res[1] if isinstance(res, tuple) else res
    for k in custom_chatbot:
        if k in text:
            r = custom_chatbot[k]
            res = r() if callable(r) else r
            return res[1] if isinstance(res, tuple) else res
    match = difflib.get_close_matches(text, custom_chatbot.keys(), n=1, cutoff=0.85)
    if match:
        r = custom_chatbot[match[0]]
        res = r() if callable(r) else r
        return res[1] if isinstance(res, tuple) else res
    try:
        response = cohere_client.chat(model='command-r', message=text)
        full_text = response.text.strip()
        limited_text = '. '.join(full_text.split('. ')[:2]).strip()
        if not limited_text.endswith('.'):
            limited_text += '.'
        return limited_text
    except Exception as e:
        print(f"[ERROR] Cohere exception: {e}")
        return "Sorry, I couldn't come up with a good answer."

# ========== Face Recognition ===========
def start_face_recognition():
    face_recognition_active[0] = True
    cap = cv2.VideoCapture(CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    while face_recognition_active[0]:
        ret, frame = cap.read()
        if not ret:
            continue
        resized_frame = cv2.resize(frame, (0, 0), fx=(1/CV_SCALER), fy=(1/CV_SCALER))
        rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
        locations = face_recognition.face_locations(rgb_frame, model=FACE_MODEL)
        encodings = face_recognition.face_encodings(rgb_frame, locations)
        for encoding in encodings:
            matches = face_recognition.compare_faces(known_face_encodings, encoding)
            name = "Unknown"
            distances = face_recognition.face_distance(known_face_encodings, encoding)
            if distances.size > 0:
                best_index = distances.argmin()
                if matches[best_index]:
                    name = known_face_names[best_index]
            shared_data["name"] = name
            speak(f"Hi, {name}")
            face_recognition_active[0] = False
            break
    cap.release()
    cv2.destroyAllWindows()

# ========== Audio Listener ===========
def audio_listener(audio_active):
    recognizer = sr.Recognizer()
    while True:
        if not audio_active[0]:
            time.sleep(0.1)
            continue
        try:
            with sr.Microphone(device_index=MICROPHONE_INDEX) as source:
                recognizer.adjust_for_ambient_noise(source)
                print("Listening...")
                audio = recognizer.listen(source, timeout=3)
                text = recognizer.recognize_google(audio)
                print(f"[DEBUG] Heard: {text}")
                AUDIO_QUEUE.put(text)
        except Exception as e:
            AUDIO_QUEUE.put("")

def run_voice_loop():
    threading.Thread(target=audio_listener, args=(audio_active,), daemon=True).start()
    while True:
        if not AUDIO_QUEUE.empty():
            text = AUDIO_QUEUE.get()
            if not text:
                continue
            audio_active[0] = False
            response = get_response(text)
            if response == "trigger_face_recognition":
                face_recognition_active[0] = True
                threading.Thread(target=start_face_recognition, daemon=True).start()
            else:
                speak(response)
            audio_active[0] = True
        time.sleep(0.1)

# ========== Web Interface ===========
HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>DARCY Web Control</title>
    <style>button{padding:10px;margin:5px;}input{padding:10px;}</style>
</head>
<body>
    <h1>DARCY Web Control</h1>
    <form method="post">
        <button name="action" value="nice to meet you">Shake</button>
        <button name="action" value="darcy">Hi</button>
        <button name="action" value="greetings">Rose</button>
        <button name="action" value="grab">Grab</button>
        <button name="action" value="release">Release</button>
        <button name="action" value="beat me">Punch</button>
        <button name="action" value="hello">Face Recognition</button><br><br>
        <input type="text" name="text" placeholder="Type to speak...">
        <button name="action" value="speak">Speak</button>
    </form>
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def control():
    if request.method == "POST":
        action = request.form.get("action")
        text = request.form.get("text")
        if action == "speak" and text:
            speak(text)
        elif action == "hello":
            threading.Thread(target=start_face_recognition, daemon=True).start()
        else:
            response = get_response(action)
            if response != "trigger_face_recognition":
                speak(response)
        return redirect("/")
    return render_template_string(HTML)

# ========== Main Entry ===========
if __name__ == "__main__":
    threading.Thread(target=run_voice_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=5005, debug=True)

