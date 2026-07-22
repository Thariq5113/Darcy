[README (1).md](https://github.com/user-attachments/files/30259532/README.1.md)
# AI Voice-Assisted Welcome Robot 🤖

A humanoid welcome/reception robot built on **Raspberry Pi 5** that combines face recognition, speech recognition, text-to-speech, and servo-driven gestures to deliver personalized greetings and simple physical interactions.

---

## ✨ Features

- **Face Recognition** — Detects and identifies visitors in real time using a pre-trained `encodings.pickle` face database, then greets known people by name.
- **Voice Interaction** — Listens continuously via microphone, converts speech to text (Google Speech Recognition, with optional offline PocketSphinx support), and responds through a rule-based intent engine.
- **Custom Chatbot Engine** — A lightweight intent-matching system (exact match → keyword containment → fuzzy matching via `difflib`) covering greetings, time/date queries, general conversation, and command handling.
- **Servo-Driven Gestures** — Drives 12+ servo motors through an I2C PWM driver board to perform physical actions (wave, handshake, grab, release) in response to voice commands or recognized faces.
- **Text-to-Speech** — Converts responses to speech using `pyttsx3`, played back through a configurable audio output device.
- **Live Camera Feed** — Displays the camera stream with real-time face bounding boxes, name labels, and an FPS counter.
- **Manual Trigger Fallback** — Keyboard-based command trigger (`h` key) as a backup input method when audio input is unavailable.
- **Multi-threaded Architecture** — Camera processing, audio listening, and the main control loop run concurrently for responsive behavior.

---

## 🛠️ Hardware

| Component | Purpose |
|---|---|
| Raspberry Pi 5 | Main compute unit |
| USB/CSI Camera | Face recognition + live video feed |
| Microphone | Voice command input |
| Speaker | Audio output (TTS responses) |
| Servo Motors (12+) | Physical gestures (wave, handshake, grab, release) |
| I2C PWM Driver Board | Servo motor control |

---

## 📦 Software Dependencies

- Python 3.x
- `opencv-python` (`cv2`)
- `face_recognition`
- `sounddevice`
- `SpeechRecognition`
- `pyttsx3`
- `gTTS`
- `numpy`
- `torch`
- `pickle` (standard library)

Install dependencies:

```bash
pip install opencv-python face_recognition sounddevice SpeechRecognition pyttsx3 gTTS numpy torch
```

> **Note:** `face_recognition` depends on `dlib`, which may require additional system-level build tools on Raspberry Pi OS (`cmake`, `build-essential`, etc.).

---

## 📁 Project Structure

```
.
├── main.py               # Main control loop (this file)
├── gesf1.py              # Servo gesture module (hello_action, grab_action, release_action)
├── gesf2.py              # Servo gesture module (wave_action, etc.)
├── encodings.pickle      # Pre-generated face encodings + names
└── README.md
```

---

## ⚙️ Configuration

Key parameters are defined at the top of the main script:

```python
CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
CV_SCALER = 4
SPEAKER_INDEX = 0
MICROPHONE_INDEX = 1
USE_POCKETSPHINX = False   # True for offline speech recognition
FACE_MODEL = 'hog'         # 'hog' for speed, 'large' (cnn) for accuracy
```

Update `CAMERA_INDEX`, `SPEAKER_INDEX`, and `MICROPHONE_INDEX` to match your connected hardware (check with `arecord -l` / `v4l2-ctl --list-devices` on Raspberry Pi OS).

The face encodings path is currently hardcoded:

```python
/home/ecerobo/encodings.pickle

## 🚀 Usage

1. Generate a face encodings file (`encodings.pickle`) containing known faces and names.
2. Connect the camera, microphone, speaker, and servo driver board.
3. Run the main script:

```bash
python3 main.py
```

4. Speak a command (e.g., *"hello"*, *"hi"*, *"darcy"*) or press **`h`** on the keyboard to manually trigger the greeting flow.
5. Say a phrase containing **"shut down"** to gracefully exit the program.

---

## 🗣️ Example Voice Commands

| Command | Behavior |
|---|---|
| `hello` | Triggers face recognition and greets the visitor by name |
| `darcy` | Waves and greets |
| `greetings` | Performs a handshake gesture |
| `hold` | Executes grab action |
| `release` | Executes release action |
| `what's the time` | Speaks the current time |
| `stop` / `wait` / `relax` | Conversational acknowledgment responses |

---

## 🧩 Known Limitations / Future Improvements

- Hardcoded file paths (e.g., `encodings.pickle`) should be made configurable via environment variables or a config file.
- Error handling around missing hardware (camera/mic) currently falls back to print statements; could be extended to a more robust degraded mode.
- `difflib` fuzzy matching handles simple typos but does not scale well to a larger intent set — consider migrating to an NLU library if the command set grows.
- No persistent conversation/session state between runs.

---

