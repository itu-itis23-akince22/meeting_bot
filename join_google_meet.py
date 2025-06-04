from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import time
import os
from dotenv import load_dotenv

load_dotenv()

class GoogleMeetBot:
    def __init__(self):
        self.mail_address = os.getenv('EMAIL_ID')
        self.password = os.getenv('EMAIL_PASSWORD')

        options = Options()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--headless')  # Disable for debugging
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.media_stream_mic": 1,
            "profile.default_content_setting_values.media_stream_camera": 1,
            "profile.default_content_setting_values.geolocation": 0,
            "profile.default_content_setting_values.notifications": 1
        })

        self.driver = webdriver.Chrome(options=options)

    def login(self):
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
        print("Google login completed.")

    def disable_microphone_and_camera(self, meet_link):
        self.driver.get(meet_link)
        time.sleep(5)

        # Disable microphone
        try:
            self.driver.find_element(By.CSS_SELECTOR, 'div[jscontroller="t2mBxb"][data-anchor-id="hw0c9"]').click()
            print("Microphone turned off.")
        except:
            print("Microphone button not found.")

        # Disable camera
        try:
            self.driver.find_element(By.CSS_SELECTOR, 'div[jscontroller="bwqwSd"][data-anchor-id="psRWwc"]').click()
            print("Camera turned off.")
        except:
            print("Camera button not found.")

    def ask_to_join(self):
        time.sleep(5)
        try:
            self.driver.find_element(By.CSS_SELECTOR, 'button[jsname="Qx7uuf"]').click()
            print("'Ask to join' button clicked.")
        except:
            print("Already joined or 'Ask to join' button not found.")

    def wait_until_meeting_ends(self):
        try:
            while True:
                self.driver.find_element(By.CSS_SELECTOR, 'button[jsname="CQylAd"]')
                time.sleep(2)
        except (NoSuchElementException, WebDriverException):
            print("Meeting ended.")

    def start(self):
        meet_link = os.getenv('MEET_LINK')
        self.login()
        self.disable_microphone_and_camera(meet_link)
        self.ask_to_join()
        self.wait_until_meeting_ends()

# If you need to test standalone (not recommended in deployed app)
if __name__ == "__main__":
    bot = GoogleMeetBot()
    bot.start()
