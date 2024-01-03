from typing import List, Tuple, Union

from sqlalchemy.ext.asyncio import AsyncSession

import models.user as Model
from database import get_session

async def gag(discord_id: int) -> Model.User | None:
    db: AsyncSession
    async with get_session() as db:
        user = await db.get(Model.User, discord_id)
        if not user:
            return None
        user.role_lock = True
        await db.commit()
        return user

async def ungag(discord_id: int) -> Model.User | None:
    db: AsyncSession
    async with get_session() as db:
        user = await db.get(Model.User, discord_id)
        if not user:
            return None
        user.role_lock = False
        await db.commit()
        return user