from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

base_dir = Path(__file__).resolve().parent.parent
dotenv_path = base_dir / '.env'


class Settings(BaseSettings):
    base_url: str = "321"
    token: str = "123"
    gemini_api: str = "Hello world"

    model_config = SettingsConfigDict(
        env_file=dotenv_path,
        env_file_encoding="utf-8",
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()
