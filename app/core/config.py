from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    MONGODB_URL: str
    DATABASE_NAME: str
    REDIS_URL: str

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), "../../.env")

settings = Settings()
