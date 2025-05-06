

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str

    class Config:
        env_file = ".env"
