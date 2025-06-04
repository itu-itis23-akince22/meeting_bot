from flask import Flask
import threading
import time
from join_google_meet import main as start_bot  

app = Flask(__name__)

@app.route('/')
def home():
    return "Google Meet Bot is running!"

@app.route('/health')
def health():
    return "OK", 200

def run_bot():
    time.sleep(5)  
    start_bot()

if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=10000)
