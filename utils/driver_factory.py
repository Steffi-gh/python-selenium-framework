import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService

def _chrome_options():
    options = webdriver.ChromeOptions()

    options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    options.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        },
    )

    options.add_argument(
        "--disable-features=PasswordLeakDetection,PasswordManagerOnboarding"
    )

    options.add_argument("--window-size=1920,1080")

    return options


def _firefox_options():
    options = webdriver.FirefoxOptions()

    options.add_argument("-headless")
    options.set_preference("remote.active-protocols", 1)
    options.add_argument("--width=1920")
    options.add_argument("--height=1080")

    # Firefox stability preferences for CI
    options.set_preference("network.http.connection-timeout", 180)
    options.set_preference("browser.sessionstore.resume_from_crash", False)
    options.set_preference("dom.ipc.processCount", 1)

    return options


def _edge_options():
    options = webdriver.EdgeOptions()

    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    return options


def get_driver(browser: str):

    browser = browser.lower()

    if browser == "chrome":
        driver = webdriver.Chrome(
            options=_chrome_options()
        )

    elif browser == "firefox":

        service = FirefoxService(
            log_output="geckodriver.log",
            service_args=["--log", "debug"]
        )
        
        service.env = os.environ.copy()

        driver = webdriver.Firefox(
            service=service,
            options=_firefox_options()
           
        )

        driver.set_page_load_timeout(120)
        driver.implicitly_wait(5)

    elif browser == "edge":
        driver = webdriver.Edge(
            options=_edge_options()
        )

    else:
        raise ValueError(f"Unsupported browser: {browser}")

    return driver