import os
from dotenv import load_dotenv

load_dotenv()

VISION_API_KEY = os.environ.get("VISION_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")