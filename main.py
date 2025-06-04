import threading
import time
from flask import Flask
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

def run_bot():
    recorder.start_recording()
    bot.start()
    time.sleep(int(os.getenv('RECORDING_DURATION', 3600)))
    recorder.stop_and_save()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=10000)
