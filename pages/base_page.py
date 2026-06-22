#This gives you reusable actions for all pages.
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import get_logger
import allure
from allure_commons.types import AttachmentType

class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.log, self.log_path = get_logger()

    def _attach_screenshot(self, name="screenshot"):
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=name,
            attachment_type=AttachmentType.PNG
        )

    def _attach_logs(self):
        allure.attach.file(
            self.log_path,
            name="logs",
            attachment_type=AttachmentType.TEXT
        )

    @allure.step("Click element: {locator}")
    def click(self, locator):
        self.log.info(f"Clicking element: {locator}")
        try:
            self.wait.until(EC.element_to_be_clickable(locator)).click()
            self._attach_screenshot()
            self._attach_logs()
        except Exception as e:
            self._attach_screenshot("error_screenshot")
            self._attach_logs()
            self.log.error(f"Error clicking element {locator}: {e}")
            raise e


    @allure.step("Type '{text}' into element: {locator}")
    def type(self, locator, text):
        self.log.info(f"Typing into element: {locator} -> {text}")
        try:
            self.wait.until(EC.visibility_of_element_located(locator)).send_keys(text)
            self._attach_screenshot()
            self._attach_logs()
        except Exception as e:
            self._attach_screenshot("error_screenshot")
            self._attach_logs()
            self.log.error(f"Error clicking element {locator}: {e}")
            raise e
    

    @allure.step("Get text from element: {locator}")
    def get_text(self, locator):
        self.log.info(f"Getting text from element: {locator}")
        try:
            text=self.wait.until(EC.visibility_of_element_located(locator)).text
            self._attach_screenshot()
            self._attach_logs()
            return text       
        except Exception as e:
            self._attach_screenshot("error_screenshot")
            self._attach_logs()
            self.log.error(f"Error clicking element {locator}: {e}")
            raise e 

