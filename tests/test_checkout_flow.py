from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

def test_checkout_flow(driver):
    driver.get("https://www.saucedemo.com")

    login = LoginPage(driver)
    login.login("standard_user", "secret_sauce")

    inventory = InventoryPage(driver)
    assert inventory.is_loaded()

    inventory.add_backpack_to_cart()
    inventory.go_to_cart()

    cart = CartPage(driver)
    assert cart.has_items()

    cart.click_checkout()

    checkout = CheckoutPage(driver)
    checkout.fill_details("Steffi", "QA", "2000")
    checkout.finish_order()

    success_message = checkout.get_success_message()
    assert "THANK YOU FOR YOUR ORDER" in success_message.upper()
