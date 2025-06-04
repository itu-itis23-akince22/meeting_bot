import threading
import time
import os
from flask import Flask, request
from record_audio import AudioRecorder
from join_google_meet import GoogleMeetBot

app = Flask(__name__)
recorder = AudioRecorder()
bot = GoogleMeetBot()

@app.route("/")
def home():
    return "Google Meet Bot is Running"

@app.route("/health")
def health():
    return "OK"

@app.route("/upload", methods=["POST"])
def upload():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    save_path = os.path.join("recordings", file.filename)
    os.makedirs("recordings", exist_ok=True)
    file.save(save_path)
    return f"File saved to {save_path}", 200

# 🚀 Bu satırı __name__ == "__main__" olmadan başlat
def start_bot_thread():
    print("🎯 Bot thread starting...")
    threading.Thread(target=run_bot, daemon=True).start()

def run_bot():
    try:
        recorder.start_recording()
        bot.start()
        time.sleep(int(os.getenv('RECORDING_DURATION', 3600)))
        recorder.stop_and_save()
    except Exception as e:
        print(f"❌ Error in run_bot: {e}")

# Gunicorn ile çalışırken de başlatılsın:
start_bot_thread()
