from dotenv import load_dotenv
import os

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "FastAPI Boilerplate")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"