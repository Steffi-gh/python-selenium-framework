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
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def get_driver():
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

    # Also disable Chrome's "Save password" bubble UI
    options.add_argument("--disable-save-password-bubble")

    # Disable Chrome Safety Check UI
    options.add_argument("--disable-features=PasswordLeakDetection,PasswordManagerOnboarding")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver