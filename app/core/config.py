from pydantic_settings import BaseSettings
import logging

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # این خط را اضافه کنید:
        logging.info(f"✅ DATABASE_URL from config: {self.DATABASE_URL}")

    class Config:
        env_file = ".env"

settings = Settings()
