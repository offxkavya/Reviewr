from openai import OpenAI
from app.core.config import settings

def get_openai_client() -> OpenAI:
    if not settings.OPENAI_API_KEY:
        return None
    return OpenAI(api_key=settings.OPENAI_API_KEY)
