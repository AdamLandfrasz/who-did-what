from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    project_name:str = "who-did-what"
    project_version:str = "1.0.0"

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()