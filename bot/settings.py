from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    DOMAIN: str
    MODE: str
    HOST: str

    class Config:
        env_file = ".env"


settings = Settings()
