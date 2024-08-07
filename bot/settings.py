from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    DOMAIN: str
    MODE: str
    HOST: str
    WEB_HOST: str
    PORT: int

    class Config:
        env_file = ".env"


settings = Settings()
