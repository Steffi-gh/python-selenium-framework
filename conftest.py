import pytest
import shutil
from utils.driver_factory import get_driver
import allure


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")


@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser")

    # Create driver (Firefox gets a fresh profile inside get_driver)
    driver = get_driver(browser)

    yield driver

    # Safe teardown
    try:
        driver.quit()
    except Exception:
        pass

    # Cleanup Firefox temp profile if present
    if hasattr(driver, "temp_profile"):
        shutil.rmtree(driver.temp_profile, ignore_errors=True)


# Attach screenshots for ANY failure (setup, call, teardown)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.failed:
        driver = item.funcargs.get("driver", None)

        if driver and hasattr(driver, "get_screenshot_as_png"):
            try:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name=f"{rep.when}_screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception:
                pass
