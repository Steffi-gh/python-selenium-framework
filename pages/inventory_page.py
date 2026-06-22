from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC

class InventoryPage(BasePage):

    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    ADD_TO_CART_BTN = (By.ID, "add-to-cart-sauce-labs-backpack")
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")

    def is_loaded(self):
        self.wait.until(EC.visibility_of_element_located(self.INVENTORY_CONTAINER))
        return "inventory" in self.driver.current_url

    def add_backpack_to_cart(self):
        self.wait.until(EC.element_to_be_clickable(self.ADD_TO_CART_BTN))  
        self.click(self.ADD_TO_CART_BTN)

    def go_to_cart(self):
        self.click(self.CART_ICON)
