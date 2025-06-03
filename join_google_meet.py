from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
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
        opt = Options()
        opt.add_argument('--disable-blink-features=AutomationControlled')
        opt.add_argument('--start-maximized')
        opt.add_experimental_option("prefs", {
            "profile.default_content_setting_values.media_stream_mic": 1,
            "profile.default_content_setting_values.media_stream_camera": 1,
            "profile.default_content_setting_values.geolocation": 0,
            "profile.default_content_setting_values.notifications": 1
        })
        self.driver = webdriver.Chrome(options=opt)

    def Glogin(self):
        self.driver.get('https://accounts.google.com/ServiceLogin?hl=en')
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.ID, "identifierId"))
        ).send_keys(self.mail_address)
        self.driver.find_element(By.ID, "identifierNext").click()
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.NAME, "Passwd"))
        ).send_keys(self.password)
        self.driver.find_element(By.ID, "passwordNext").click()
        time.sleep(5)
        print("Gmail login activity complete.")

    def turnOffMicCam(self, meet_link):
        self.driver.get(meet_link)
        time.sleep(5)
        try:
            self.driver.find_element(By.CSS_SELECTOR, 'div[jscontroller="t2mBxb"][data-anchor-id="hw0c9"]').click()
            print("Microphone turned off.")
        except:
            print("Mic button not found.")
        try:
            self.driver.find_element(By.CSS_SELECTOR, 'div[jscontroller="bwqwSd"][data-anchor-id="psRWwc"]').click()
            print("Camera turned off.")
        except:
            print("Camera button not found.")

    def AskToJoinAndRecord(self, recorder, mp3_path):
        time.sleep(5)
        try:
            self.driver.find_element(By.CSS_SELECTOR, 'button[jsname="Qx7uuf"]').click()
            print("Ask to join clicked.")
        except:
            print("Already joined or ask button not found.")

        recorder.start_recording()
        print("Recording started during meeting...")

        try:
            while True:
                self.driver.find_element(By.CSS_SELECTOR, 'button[jsname="CQylAd"]') 
                time.sleep(2)
        except NoSuchElementException:
            print("Meeting ended. Stopping recording.")
            recorder.stop_and_save(mp3_path)

def main():
    temp_dir = tempfile.mkdtemp()
    mp3_path = os.path.join(temp_dir, "meeting_recording.mp3")
    meet_link = os.getenv('MEET_LINK')

    obj = JoinGoogleMeet()
    recorder = AudioRecorder()
    obj.Glogin()
    obj.turnOffMicCam(meet_link)
    obj.AskToJoinAndRecord(recorder, mp3_path)

    print(f"MP3 kaydı burada: {mp3_path}")

if __name__ == "__main__":
    main() 