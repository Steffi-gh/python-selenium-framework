import pytest
import shutil
from utils.driver_factory import get_driver
import allure


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")


import time

@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser")

    # try a couple of times to create the driver
    last_exc = None
    for attempt in range(2):
        try:
            driver = get_driver(browser)
            break
        except Exception as e:
            last_exc = e
            time.sleep(3)
    else:
        # re-raise the last exception so pytest records setup failure
        raise last_exc

    yield driver

    try:
        driver.quit()
    except Exception:
        pass

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
