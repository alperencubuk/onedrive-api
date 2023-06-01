from functools import lru_cache

# Third Party Packages
from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_TITLE: str = "OneDrive API"
    VERSION: str = "1.0.0"
    CLIENT_ID: str
    CLIENT_SECRET: str
    CALLBACK_URL: str = "http://localhost:8000/onedrive/callback"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
