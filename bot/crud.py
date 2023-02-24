from typing import List, Optional

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

import models as m
import schemas as s
from db import async_session


class UserDAL:
    def __init__(self, db_session: AsyncSession):
        self.db: AsyncSession = db_session

    async def create_user(
        self,
        discord_id: int,
    ) -> s.User:
        db_user = s.UserCreate(discord_id=discord_id)
        await self.db.add(db_user.dict())
        await self.db.commit()
        return db_user

    async def update_user(
        self,
        discord_id: int,
        badwords: Optional[List[str]],
        owned_by: Optional[int],
        properties: Optional[List[int]],
        claimed_by: Optional[int],
    ):
        q = update(m.User).where(m.User.discord_id == discord_id)
        if badwords:
            q = q.values(badwords=badwords)
        if owned_by:
            q = q.values(owned_by=owned_by)
        if properties:
            q = q.values(properties=properties)
        if claimed_by:
            q = q.values(claimed_by=claimed_by)
        q.execution_options(synchronize_session="fetch")
        await self.db.execute(q)

    async def get_user_badwords(self, discord_id: int) -> List[str]:
        user: s.User = await self.db.get(m.User.discord_id == discord_id)
        return user.bad_words.copy()

    async def get_user_owner(self, discord_id: int) -> int:
        user: s.User = await self.db.get(m.User.discord_id, discord_id)
        return user.owned_by

    async def get_user_properties(self, discord_id: int) -> List[int]:
        user: s.User = await self.db.get(m.User.discord_id, discord_id)
        return user.properties.copy()

    async def get_user_claimed_by(self, discord_id: int) -> int:
        user: s.User = await self.db.get(m.User.discord_id, discord_id)
        return user.claimed_by


async def get_user_dal() -> UserDAL:
    async with async_session() as sess:
        async with sess.begin():
            yield UserDAL(sess)
