import logging
import os

def get_logger(name="automation"):
    logs_dir = "logs"
    os.makedirs(logs_dir, exist_ok=True)

    log_path = os.path.join(logs_dir, "framework.log")

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers
    if not logger.handlers:
        file_handler = logging.FileHandler(log_path, mode="w")
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger, log_path

import allure
def attach_logs():
    with open("logs/framework.log", "r") as f:
        allure.attach(f.read(), name="Logs", attachment_type=allure.attachment_type.TEXT)
