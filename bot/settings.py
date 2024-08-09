from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    DOMAIN: str
    MODE: str
    HOST: str
    WEB_HOST: str
    PORT: int
    DEFAULT_ROLE_ID: str

    # Database credentials
    MONGO_HOST: str
    MONGO_PORT: int
    MONGO_NAME: str
    MONGO_TZ_AWARE: bool

    class Config:
        env_file = ".env"


settings = Settings()
