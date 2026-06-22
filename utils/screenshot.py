import os
from datetime import datetime

def take_screenshot(driver, name="screenshot"):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs("screenshots", exist_ok=True)
    file_path = f"screenshots/{name}_{timestamp}.png"
    driver.save_screenshot(file_path)
    return file_path

import allure

def attach_screenshot(driver, name="screenshot"):
    png = driver.get_screenshot_as_png()
    allure.attach(png, name=name, attachment_type=allure.attachment_type.PNG)

def attach_logs():
    with open("logs/framework.log", "r") as f:
        allure.attach(f.read(), name="Logs", attachment_type=allure.attachment_type.TEXT)