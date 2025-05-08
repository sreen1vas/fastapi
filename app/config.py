# app/config.py
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    database_hostname: str = Field(..., alias="DATABASE_HOSTNAME")
    database_port: int = Field(..., alias="DATABASE_PORT")
    database_name: str = Field(..., alias="DATABASE_NAME")
    database_username: str = Field(..., alias="DATABASE_USERNAME")
    database_password: str = Field(..., alias="DATABASE_PASSWORD")

    secret_key: str = Field(..., alias="SECRET_KEY")
    algorithm: str = Field(..., alias="ALGORITHM")
    access_token_expire_minutes: int = Field(..., alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    class Config:
        env_file = ".env"
        populate_by_name = True

settings = Settings()  # ✅ Required for your import to work
