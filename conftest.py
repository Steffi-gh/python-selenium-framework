import time
import shutil
import pytest
import allure

from utils.driver_factory import get_driver


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome"
    )


@pytest.fixture
def driver(request):

    browser = request.config.getoption("--browser")

    last_exception = None

    for attempt in range(2):
        try:
            driver = get_driver(browser)
            break

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            last_exception = e
            time.sleep(5)

    else:
        raise last_exception

    yield driver

    try:
        driver.quit()
    except Exception:
        pass

    if hasattr(driver, "temp_profile"):
        shutil.rmtree(driver.temp_profile, ignore_errors=True)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    if report.failed:

        driver = item.funcargs.get("driver")

        if driver:

            try:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name=f"{report.when}_failure",
                    attachment_type=allure.attachment_type.PNG,
                )

            except Exception:
                pass