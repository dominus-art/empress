from sqlalchemy.ext.asyncio import AsyncSession

import models.user as Model


async def create_user(db: AsyncSession, discord_id: int) -> Model.User:
    user = Model.User(discord_id=discord_id)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
