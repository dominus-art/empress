from typing import List

from pydantic import BaseModel


class UserBase(BaseModel):
    owned_by: int
    properties: List[str]
    bad_words: List[str]
    claimed_by: int
    lives: int


class UserCreate(UserBase):
    discord_id: str


class User(UserBase):
    class Config:
        orm_mode = True
