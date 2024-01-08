from typing import List, Dict
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    DISCORD_TOKEN: str
    PREFIX: str
    DEFAULT_COGS: List[str]
    SNIPE_CACHE_SIZE: int
    GUILD_ID: int
    TECH_CHANNEL: int

    SQLITE_URI: str
    DB_NAME: str

    ADMIN_ROLES: List[int]
    TECH_ROLE: int
    BADWORDS_ROLE: int
    PEACE_ROLE: int
    DOM_ROLE: int
    SWITCH_ROLE: int
    SUB_ROLE: int
    GAG_ROLES: Dict[str, int]

    NOMEDIA_ROLE: int
    NOREACTIONS_ROLE: int
    NOSPEECH_ROLE: int
    NONSFW_ROLE: int

    class Config:
        env_file = "~/personal-projects/empress/env/bot.env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
