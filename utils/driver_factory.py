#This ensures:
#No manual driver downloads
#Chrome auto‑updates
#Tests run on any machine

#from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager

#def get_driver():
#    options = webdriver.ChromeOptions()
#    options.add_argument("--start-maximized")
#    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
#    return driver


from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

from selenium.webdriver.edge.service import Service as EdgeService

from webdriver_manager.chrome import ChromeDriverManager

import tempfile

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
        firefox_options.add_argument("--headless=new")
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-dev-shm-usage")
        firefox_options.add_argument("--width=1920")
        firefox_options.add_argument("--height=1080")

        # Use ONLY the fresh profile
        firefox_options.add_argument(f"--profile={profile_path}")

        # CI stability fixes
        firefox_options.set_preference("browser.tabs.remote.autostart", False)
        firefox_options.set_preference("browser.tabs.remote.autostart.1", False)
        firefox_options.set_preference("browser.tabs.remote.autostart.2", False)
        firefox_options.set_preference("browser.tabs.remote.force-enable", False)
        firefox_options.set_preference("browser.tabs.remote.separatePrivilegedContentProcess", False)
        firefox_options.set_preference("browser.tabs.remote.separatePrivilegedJavaScriptProcess", False)
        firefox_options.set_preference("dom.ipc.processCount", 1)
        firefox_options.set_preference("network.proxy.type", 0)
        firefox_options.set_preference("browser.sessionstore.resume_from_crash", False)

        return webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=firefox_options
        )




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
