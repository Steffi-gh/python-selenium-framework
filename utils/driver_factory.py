import tempfile
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def get_driver(browser: str, profile_path: str = None):
    browser = browser.lower()

    # -----------------------------
    # CHROME (CI-safe)
    # -----------------------------
    if browser == "chrome":
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Disable Chrome password manager popups
        chrome_options.add_experimental_option("prefs", {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
            "password_manager_enabled": False,
            "profile.default_content_setting_values.notifications": 2
        })

        chrome_options.add_argument("--disable-save-password-bubble")
        chrome_options.add_argument("--disable-features=PasswordLeakDetection,PasswordManagerOnboarding")

        return webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options
        )

    # -----------------------------
    # FIREFOX (CI-safe, stable)
    # -----------------------------
    elif browser == "firefox":
        import os
        from selenium.webdriver.firefox.service import Service as FirefoxService
        from webdriver_manager.firefox import GeckoDriverManager

        log_path = f"/tmp/geckodriver-{os.getpid()}.log"
        service = FirefoxService(GeckoDriverManager().install(), log_path=log_path)

        # Create a fresh profile per test (critical for CI stability)
        temp_profile = tempfile.mkdtemp()
        firefox_options = webdriver.FirefoxOptions()

        firefox_options.add_argument("--headless")
        firefox_options.add_argument("--width=1920")
        firefox_options.add_argument("--height=1080")

        # Use ONLY the fresh profile
        firefox_options.add_argument(f"--profile={temp_profile}")

        # Disable Firefox multi-process (critical for GitHub Actions)
        firefox_options.set_preference("browser.tabs.remote.autostart", False)
        firefox_options.set_preference("browser.tabs.remote.autostart.1", False)
        firefox_options.set_preference("browser.tabs.remote.autostart.2", False)
        firefox_options.set_preference("browser.tabs.remote.force-enable", False)
        firefox_options.set_preference("browser.tabs.remote.separatePrivilegedContentProcess", False)
        firefox_options.set_preference("browser.tabs.remote.separatePrivilegedJavaScriptProcess", False)
        firefox_options.set_preference("dom.ipc.processCount", 1)

        # CI stability
        firefox_options.set_preference("network.proxy.type", 0)
        firefox_options.set_preference("browser.sessionstore.resume_from_crash", False)

        driver = webdriver.Firefox(
            service=service,
            options=firefox_options,
            # timeout increases the time to wait for the driver to start/respond
            timeout=180
        )

        # attach path so fixture/CI can upload it on failure
        driver.geckodriver_log = log_path
        # Attach cleanup path to driver so fixture can delete it
        driver.temp_profile = temp_profile
        return driver

    # -----------------------------
    # EDGE (CI-safe)
    # -----------------------------
    elif browser == "edge":
        edge_options = webdriver.EdgeOptions()
        edge_options.add_argument("--headless=new")
        edge_options.add_argument("--disable-gpu")
        edge_options.add_argument("--no-sandbox")
        edge_options.add_argument("--disable-dev-shm-usage")

        return webdriver.Edge(
            service=EdgeService(EdgeChromiumDriverManager().install()),
            options=edge_options
        )

    else:
        raise Exception(f"Browser '{browser}' is not supported")
