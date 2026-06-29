Automation Framework README
Python Selenium Automation Framework
A scalable UI automation framework built with Python, Selenium WebDriver, PyTest, Allure Reporting, and GitHub Actions. Supports parallel execution, multi-browser testing, and Page Object Model architecture.
________________________________________
Features
•	Python + Selenium + PyTest test automation
•	Page Object Model (POM) structure
•	Multi-browser execution (Chrome, Firefox, Edge)
•	Parallel execution using pytest-xdist
•	Allure reporting with screenshots and history
•	GitHub Actions CI/CD with browser matrix
•	CI-safe driver factory for stable execution
•	Automatic Allure report deployment to GitHub Pages
________________________________________
Project Structure
python-selenium-framework/
│
├── tests/
│   ├── test_login.py
│   ├── test_checkout_flow.py
│
├── pages/
│   ├── base_page.py
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── checkout_page.py
│
├── utils/
│   ├── driver_factory.py
│
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md
________________________________________
Technology Stack
Component	Description
Python 3.11	Programming language
Selenium WebDriver	Browser automation
PyTest	Test runner
pytest-xdist	Parallel execution
Allure	Reporting
GitHub Actions	CI/CD pipeline
Page Object Model	Test architecture
________________________________________
Running Tests
Chrome
pytest -n auto --browser=chrome --alluredir=allure-results/chrome
Firefox
pytest -n auto --browser=firefox --alluredir=allure-results/firefox
Edge
pytest -n auto --browser=edge --alluredir=allure-results/edge
________________________________________
Parallel Execution
Parallel execution is enabled using pytest-xdist:
pytest -n auto
This automatically uses all available CPU cores.
________________________________________
Allure Reporting
Generate report locally:
allure generate allure-results -o allure-report --clean
allure open allure-report
The CI pipeline automatically:
•	Generates per-browser results
•	Merges results
•	Deploys the final report to GitHub Pages
Live report: https://steffi-gh.github.io/python-selenium-framework/
________________________________________
CI/CD Pipeline
The GitHub Actions workflow:
•	Installs Chrome, Firefox, and Edge
•	Installs matching drivers
•	Executes tests in parallel per browser
•	Uploads per-browser Allure results
•	Merges results into a unified report
•	Deploys the report to GitHub Pages
This demonstrates real-world CI automation practices.
________________________________________
Writing Tests
Example:
def test_valid_login(driver):
    login = LoginPage(driver)
    login.open()
    login.login("standard_user", "secret_sauce")
    assert login.is_logged_in()
________________________________________
Page Object Model Example
class LoginPage(BasePage):
    def open(self):
        self.driver.get("https://www.saucedemo.com")

    def login(self, username, password):
        self.type("#user-name", username)
        self.type("#password", password)
        self.click("#login-button")
________________________________________
Setup
Install dependencies:
pip install -r requirements.txt
Run tests:
pytest -n auto --browser=chrome
________________________________________
Author
Steffi QA Automation Engineer / SDET Sydney, Australia
