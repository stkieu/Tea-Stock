from pydantic_settings import BaseSettings

#allows us to access config values
class Settings(BaseSettings):
    SECRET_KEY: str
    CLIENT_ID: str
    CLIENT_SECRET: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()