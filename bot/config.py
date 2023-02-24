from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DISCORD_TOKEN: str
    POSTGRES_HOST: str
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_URI: str = None
    PREFIX: str

    class Config:
        env_file = "~/roq-bot/env/bot.env"


@lru_cache()
def get_settings() -> Settings:
    tmp = Settings()
    return Settings(
        POSTGRES_URI="postgresql+asyncpg://{}:{}@{}:5432/{}".format(
            tmp.POSTGRES_USER,
            tmp.POSTGRES_PASSWORD,
            tmp.POSTGRES_HOST,
            tmp.POSTGRES_DB,
        )
    )
