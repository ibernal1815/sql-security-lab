import os
from dotenv import load_dotenv

# This loads environment variables from .env
# Much more secure than hardcoding passwords
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
