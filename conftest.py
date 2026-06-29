import pytest
import allure
from utils.driver_factory import get_driver

@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser")

    # Let Selenium handle the profile automatically by passing None
    driver = get_driver(browser, profile_path=None)

    yield driver

    # Safe teardown
    try:
        driver.quit()
    except Exception:
        pass

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver", None)
        if driver:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="failure_screenshot",
                attachment_type=allure.attachment_type.PNG
            )

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")