import json
from typing import List, Tuple, Union

from sqlalchemy.ext.asyncio import AsyncSession

import models.user as Model


async def add_badwords(
    db: AsyncSession, discord_id: int, badwords: List[str]
) -> Model.User:
    user: Model.User = await db.get(Model.User, discord_id)
    tmp: list = json.loads(user.bad_words)
    tmp.extend(badwords)
    user.bad_words = json.dumps(tmp)
    await db.commit()
    return user


async def remove_badwords(
    db: AsyncSession, discord_id: int, badwords: List[str]
) -> Tuple[Model.User, Union[str, List[str]]]:
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
    return (user, actions)


async def clear_badwords(db: AsyncSession, discord_id: int) -> Model.User:
    user: Model.User = await db.get(Model.User, discord_id)
    user.bad_words = json.dumps([])
    user.lives = -1
    await db.commit()
    return user


async def decrease_live(db: AsyncSession, discord_id: int) -> int:
    user: Model.User = await db.get(Model.User, discord_id)
    user.lives -= 1
    await db.commit()
    return user.lives


async def set_lives(db: AsyncSession, discord_id: int, lives: int) -> int:
    user: Model.User = await db.get(Model.User, discord_id)
    user.lives = lives
    await db.commit()
    return user.lives
