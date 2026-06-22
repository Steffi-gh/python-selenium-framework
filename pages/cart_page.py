from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):

    CART_ITEM = (By.CLASS_NAME, "cart_item")
    CHECKOUT_BTN = (By.ID, "checkout")

    def has_items(self):
        items = self.driver.find_elements(*self.CART_ITEM)
        return len(items) > 0

    def click_checkout(self):
        self.click(self.CHECKOUT_BTN)