# 🤖 Google Meet Auto-Join & Audio Recording Bot

This project is a Python-based automation tool that joins Google Meet sessions and records all system audio (including meeting participants) into an `.mp3` file. The bot uses Selenium to log in and join the meeting silently, while a separate script captures system audio.

## 📁 Project Structure

- `join_google_meet.py`: Automatically logs into Google and joins the specified Google Meet link.
- `record_audio.py`: Records all computer/system audio and saves it as an `.mp3` file.
- `.env`: Stores environment variables (email, password, Meet link, etc.).
- `requirements.txt`: Lists the Python dependencies required for the project.

---

## 🚀 Getting Started

### STEPS
Also do not forget to modify .env file
```bash
git clone https://github.com/itu-itis23-akince22/google-meet-bot.git
cd google-meet-bot
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
pip install -r requirements.txt 
python join_google_meet.py 
