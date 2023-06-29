import json
from typing import List, Tuple, Union

from sqlalchemy.ext.asyncio import AsyncSession

import models.user as Model
from database import get_session


async def add_badwords(
    discord_id: int, badwords: List[str]
) -> Model.User:
    db: AsyncSession
    async with get_session() as db:
        user: Model.User = await db.get(Model.User, discord_id)
        tmp: list = json.loads(user.bad_words)
        tmp.extend(badwords)
        user.bad_words = json.dumps(tmp)
        await db.commit()
        await db.refresh(user)
        return user


async def remove_badwords(
    discord_id: int, badwords: List[str]
) -> Tuple[Model.User, Union[str, List[str]]]:
    db: AsyncSession
    async with get_session() as db:
        user: Model.User = await db.get(Model.User, discord_id)
        tmp: list = json.loads(user.bad_words)
        if len(tmp) == 0:
            return (user, "No bad words to remove")

        actions = []
        for word in badwords:
            try:
                tmp.remove(word)
                actions.append(f"Added {word}")
            except ValueError:
                actions.append(f"{word} is not badworded for this user")

        user.bad_words = json.dumps(tmp)
        await db.commit()
        await db.refresh(user)
        return (user, actions)


async def clear_badwords(discord_id: int) -> Model.User:
    db: AsyncSession
    async with get_session() as db:
        user: Model.User = await db.get(Model.User, discord_id)
        user.bad_words = json.dumps([])
        user.lives = -1
        await db.commit()
        await db.refresh(user)
        return user


async def set_lives(discord_id: int, lives: int) -> Model.User:
    db: AsyncSession
    async with get_session() as db:
        user: Model.User = await db.get(Model.User, discord_id)
        user.lives = lives
        await db.commit()
        await db.refresh(user)
        return user
