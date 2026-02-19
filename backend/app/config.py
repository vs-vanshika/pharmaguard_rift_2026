import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")

settings = Settings()