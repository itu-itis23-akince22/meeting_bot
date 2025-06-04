from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import time
from record_audio import AudioRecorder
import os
import tempfile
from dotenv import load_dotenv

load_dotenv()

class JoinGoogleMeet:
    def __init__(self):
        self.mail_address = os.getenv('EMAIL_ID')
        self.password = os.getenv('EMAIL_PASSWORD')

        # Configure Chrome options
        options = Options()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--headless')  # Comment this out for debugging
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.media_stream_mic": 1,
            "profile.default_content_setting_values.media_stream_camera": 1,
            "profile.default_content_setting_values.geolocation": 0,
            "profile.default_content_setting_values.notifications": 1
        })

        # Initialize the WebDriver
        self.driver = webdriver.Chrome(options=options)

    def Glogin(self):
        # Open the Google login page
        self.driver.get('https://accounts.google.com/ServiceLogin?hl=en')

        # Enter email
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.ID, "identifierId"))
        ).send_keys(self.mail_address)
        self.driver.find_element(By.ID, "identifierNext").click()

        # Enter password
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.NAME, "password"))
        ).send_keys(self.password)
        self.driver.find_element(By.ID, "passwordNext").click()

        time.sleep(5)
        print("✅ Gmail login completed.")

    def turnOffMicCam(self, meet_link):
        # Open the Google Meet link
        self.driver.get(meet_link)
        time.sleep(5)

        # Turn off microphone
        try:
            self.driver.find_element(By.CSS_SELECTOR, 'div[jscontroller="t2mBxb"][data-anchor-id="hw0c9"]').click()
            print("🎙️ Microphone turned off.")
        except:
            print("⚠️ Microphone button not found.")

        # Turn off camera
        try:
            self.driver.find_element(By.CSS_SELECTOR, 'div[jscontroller="bwqwSd"][data-anchor-id="psRWwc"]').click()
            print("📷 Camera turned off.")
        except:
            print("⚠️ Camera button not found.")

    def AskToJoinAndRecord(self, recorder, mp3_path):
        # Click "Ask to join" button
        time.sleep(5)
        try:
            self.driver.find_element(By.CSS_SELECTOR, 'button[jsname="Qx7uuf"]').click()
            print("🙋 Clicked 'Ask to join'.")
        except:
            print("⏩ Already joined or 'Ask to join' button not found.")

        # Start audio recording
        recorder.start_recording()
        print("🎧 Recording started...")

        # Wait until the "Leave call" button disappears (meeting ends)
        try:
            while True:
                self.driver.find_element(By.CSS_SELECTOR, 'button[jsname="CQylAd"]')
                time.sleep(2)
        except (NoSuchElementException, WebDriverException):
            print("🏁 Meeting ended. Stopping recording.")
            recorder.stop_and_save(mp3_path)

def main():
    # Prepare temporary path to store recording
    temp_dir = tempfile.mkdtemp()
    mp3_path = os.path.join(temp_dir, "meeting_recording.mp3")
    meet_link = os.getenv('MEET_LINK')

    obj = JoinGoogleMeet()
    recorder = AudioRecorder()

    obj.Glogin()
    obj.turnOffMicCam(meet_link)
    obj.AskToJoinAndRecord(recorder, mp3_path)

    print(f"🎵 Recording saved at: {mp3_path}")

if __name__ == "__main__":
    main()
