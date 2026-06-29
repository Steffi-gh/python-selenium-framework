# utils/driver_factory.py

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def _chrome_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    # Required for GitHub Actions Linux runner
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Disable Chrome password manager + leak detection popup
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
        "password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_setting_values.popups": 0,
        "profile.default_content_setting_values.automatic_downloads": 1,
        "profile.default_content_setting_values.cookies": 1,
        "profile.default_content_setting_values.images": 1,
        "profile.default_content_setting_values.javascript": 1,
        "profile.default_content_setting_values.plugins": 1,
        "profile.default_content_setting_values.mixed_script": 1,
        "profile.default_content_setting_values.media_stream": 1,
        "profile.default_content_setting_values.geolocation": 1,
        "profile.default_content_setting_values.password_protection": 0
    })

    options.add_argument("--disable-save-password-bubble")
    options.add_argument("--disable-features=PasswordLeakDetection,PasswordManagerOnboarding")

    return options


def _firefox_options():
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return options


def _edge_options():
    options = webdriver.EdgeOptions()
    options.use_chromium = True

    # Correct headless mode for Edge (Chrome-style flags break Edge)
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    return options


def get_driver(browser: str):
    browser = browser.lower()
    driver = None  # ALWAYS define driver to avoid UnboundLocalError

    try:
        if browser == "chrome":
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=_chrome_options()
            )

        elif browser == "firefox":
            driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()),
                options=_firefox_options()
            )

        elif browser == "edge":
            driver = webdriver.Edge(
                service=EdgeService(EdgeChromiumDriverManager().install()),
                options=_edge_options()
            )

        else:
            raise ValueError(f"Unsupported browser: {browser}")

    except Exception as e:
        print(f"[driver_factory] Failed to start {browser}: {e}")
        raise

    return driver
