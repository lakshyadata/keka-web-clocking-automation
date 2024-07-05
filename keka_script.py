import os
import time
import base64
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import anthropic

load_dotenv()  # Load environment variables from .env file

class Keka:
    EMAIL = os.getenv('KEKA_EMAIL')
    PASSWORD = os.getenv('KEKA_PASSWORD')
    URL = os.getenv('KEKA_URL')
    CHECK = os.getenv('KEKA_CHECK', 'in')
    
    def extract_captcha_text(text):
        start_tag = "<captcha_text>"
        end_tag = "</captcha_text>"

        start_index = text.find(start_tag)
        if start_index == -1:
            return ""

        start_index += len(start_tag)
        end_index = text.find(end_tag)
        if end_index == -1:
            return ""
        captcha_text = text[start_index:end_index]
        captcha_text = captcha_text.upper()
        return captcha_text

    def start(self):
        browser = webdriver.Chrome()  # Make sure you have ChromeDriver installed and in PATH
        browser.get(f"{self.URL}/#/home/dashboard")
        time.sleep(5)
        # check if redirected to login page
        if 'Account/Login' in browser.current_url:
            # select keka login with password (at button.div.p with text "keka password")
            browser.find_element(By.XPATH, '//button/div/p[text()="keka password"]').click()
            time.sleep(2)
            # input email and password
            browser.find_element(By.ID, "email").send_keys(self.EMAIL)
            browser.find_element(By.ID, "password").send_keys(self.PASSWORD)
            # extract captcha image from img.imgCaptcha
            captcha_element = browser.find_element(By.CSS_SELECTOR, 'img.imgCaptcha')
            captcha_image_url = captcha_element.get_attribute('src')
            # convert captcha image to PIL Image object
            captcha_image = Image.open(BytesIO(base64.b64decode(captcha_image_url.split(',')[1])))
            # create a new image with white background
            white_background = Image.new('RGB', captcha_image.size, (255, 255, 255))
            white_background.paste(captcha_image, mask=captcha_image.split()[3])
            # convert the image back to base64
            buffered = BytesIO()
            white_background.save(buffered, format="PNG")
            captcha_image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            # pass the captcha image to Claude AI for parsing
            client = anthropic.Anthropic(os.getenv('ANTHROPIC_API_KEY'))
            message = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": captcha_image_base64,
                                },
                            },
                            {
                                "type": "text",
                                "text": "Please provide the text shown in this captcha image between <captcha_text>"
                            }
                        ],
                    }
                ],
            )
            captcha_text = message['replies'][0].strip()
            captcha_text = self.extract_captcha_text(captcha_text)
            # input the parsed captcha text
            browser.find_element(By.ID, "captcha").send_keys(captcha_text)
            # submit the login form
            browser.find_element(By.XPATH, '//button[text()="Login"]').click()

        browser.get(f"{self.URL}/#/me/attendance/logs")
        time.sleep(5)  # Wait for the page to load

        if self.CHECK.lower() == 'in':
            web_clock_in = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//a[text()="Web Clock-In"]'))
            )
            web_clock_in.click()
        elif self.CHECK.lower() == 'out':
            web_clock_out = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()="Web Clock-out"]'))
            )
            web_clock_out.click()
            browser.find_element(By.XPATH, '//button[text()="Clock-out"]').click()

        time.sleep(5)
        browser.quit()

if __name__ == '__main__':
    Keka().start()
