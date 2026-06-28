#This is your first working test.
from utils.driver_factory import get_driver
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

def test_valid_login():
    driver = get_driver()
    driver.get("https://www.saucedemo.com")
    login = LoginPage(driver)
    login.login("standard_user", "secret_sauce")
#   assert "inventory" in driver.current_url
    inventory = InventoryPage(driver)
    assert inventory.is_loaded()
    driver.quit()