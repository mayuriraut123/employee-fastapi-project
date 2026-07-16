import logging
import os

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("employee_app")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

app_handler = logging.FileHandler("logs/app.log")
app_handler.setLevel(logging.INFO)
app_handler.setFormatter(formatter)

error_handler = logging.FileHandler("logs/error.log")
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(app_handler)
    logger.addHandler(error_handler)