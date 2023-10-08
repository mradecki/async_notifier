from functools import lru_cache

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_uri: PostgresDsn
    sleep_time: int = 5  # default value
    max_retries: int = 3  # default value


# Create a global instance of the settings
settings = Settings()
