

from flask import Flask, render_template, request
from s import (
    shake_hand_action, punch_action, rose_action,
    salute_action, grab_action, release_action,
    rightnormal_servos, leftnormal_servos
)

app = Flask(__name__, template_folder='webpages')
status_message = ""

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', status="Welcome to Darcy's World")

@app.route('/action', methods=['POST'])
def perform_action():
    action = request.form.get('action')
    status = "Unknown action"

    if action == 'shake':
        shake_hand_action()
        status = "Shake Hand Completed!"
    elif action == 'punch':
        punch_action()
        status = "Punch Completed!"
    elif action == 'rose':
        rose_action()
        status = "Rose Given!"
    elif action == 'salute':
        salute_action()
        status = "Salute Completed!"
    elif action == 'grab':
        grab_action()
        status = "Grabbed!"
    elif action == 'release':
        release_action()
        status = "Released!"
    elif action == 'reset':
        rightnormal_servos()
        leftnormal_servos()
        status = "Servos Reset to Normal"

    return render_template('index.html', status=status)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
