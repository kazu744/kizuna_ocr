import os
from dotenv import load_dotenv

load_dotenv()

VISION_API_KEY = os.environ.get("VISION_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

DB_DIALECT = os.environ.get("DB_DIALECT")
DB_DRIVER = os.environ.get("DB_DRIVER")
DB_USER = os.environ.get("DB_USER")
DB_PASSWD = os.environ.get("DB_PASSWD")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_HOST = os.environ.get("DB_HOST")