Python + Selenium + PyTest Automation Framework
A complete, scalable UI automation framework built using Python, Selenium WebDriver, PyTest, Page Object Model (POM), Allure Reporting, and CI/CD with GitHub Actions & Azure Pipelines.

🚀 Project Overview
This framework automates the end‑to‑end UI flow of the SauceDemo sample application, including:

Login

Inventory validation

Add to cart

Checkout flow

Assertions & validations

Reporting & logs

CI execution

It is designed to demonstrate real‑world automation engineering skills, including maintainability, scalability, and CI integration.

🧱 Tech Stack
Python 3.x

Selenium WebDriver

PyTest

Page Object Model (POM)

Allure Reports

GitHub Actions

Azure DevOps Pipelines

📁 Project Structure
Code
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
|   ├── cart_page.py
|
├── utils/
│   ├── driver_factory.py
│   ├── logger.py
│
├── reports/          # pytest-html reports
├── logs/             # Framework logs
├── requirements.txt
├── pytest.ini
└── README.md
🧪 Running Tests Locally
1. Install dependencies
Code
pip install -r requirements.txt
2. Run all tests
Code
pytest
3. Run tests with Allure
Code
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
📊 Reporting
Allure Reports
Step‑by‑step execution

Screenshots on failure

Logs attached

Environment metadata

PyTest HTML Report
Automatically generated via pytest.ini.

🏗 CI/CD Integration
This project supports:

GitHub Actions (runs tests on every push)

Azure DevOps Pipelines (runs tests on demand or per PR)