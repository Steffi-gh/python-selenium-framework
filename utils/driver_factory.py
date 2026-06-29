import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager

def get_driver(browser="chrome", profile_path=None):
    browser = browser.lower()

    # -----------------------------
    # Common options (headless, CI)
    # -----------------------------
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")

    # Disable Chrome password manager + leak detection popup
    chrome_options.add_experimental_option("prefs", {
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

    chrome_options.add_argument("--disable-save-password-bubble")
    chrome_options.add_argument("--disable-features=PasswordLeakDetection,PasswordManagerOnboarding")

    # -----------------------------
    # Browser selection
    # -----------------------------
    if browser == "chrome":
        return webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options
        )

    elif browser == "firefox":
        from selenium.webdriver.firefox.service import Service as FirefoxService
        from webdriver_manager.firefox import GeckoDriverManager

        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument("--headless") 
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-dev-shm-usage")
        firefox_options.add_argument("--width=1920")
        firefox_options.add_argument("--height=1080")

        if profile_path:
            firefox_options.add_argument(f"--profile={profile_path}")

        # Basic infrastructure stability adjustments for CI
        firefox_options.set_preference("network.proxy.type", 0)
        firefox_options.set_preference("browser.sessionstore.resume_from_crash", False)
        
        # Instantiate Firefox
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=firefox_options
        )

        # FIX: Backward/forward compatible way to increase HTTP connection timeouts 
        # to 300 seconds across all Selenium 4.x versions without requiring specific imports.
        try:
            if hasattr(driver.command_executor, 'client_config'):
                driver.command_executor.client_config.timeout = 300
            else:
                driver.command_executor.set_timeout(300)
        except Exception:
            pass # Fallback safety if the runner uses an alternative setup context

        return driver

    elif browser == "edge":
        from webdriver_manager.microsoft import EdgeChromiumDriverManager
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