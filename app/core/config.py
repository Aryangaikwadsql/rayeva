"""App config."""
from functools import lru_cache
from typing import Any
from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///raveya.db"
    OPENAI_API_KEY: str | None = None
    OPENROUTER_API_KEY: str | None = None
    GROQ_API_KEY: str | None = None
    proxies: dict[str, str] | None = None

    model_config = ConfigDict(extra="ignore")


@lru_cache()
def get_settings() -> Settings:
    return Settings()
