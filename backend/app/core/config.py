import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Reviewr"
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    API_V1_STR: str = "/api"

settings = Settings()
