from sqlalchemy.ext.asyncio import AsyncSession

import models.user as Model
from database import get_session


async def create_user(discord_id: int) -> Model.User:
    db: AsyncSession
    async with get_session() as db:
        user = Model.User(discord_id=discord_id)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user


async def get_user(discord_id: int) -> Model.User:
    db: AsyncSession
    async with get_session() as db:
        return await db.get(Model.User, discord_id)
