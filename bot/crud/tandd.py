import random

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import models.tandd as Model
from database import get_session


async def create_truth(rating: int, content: str) -> Model.Truth:
    db: AsyncSession
    async with get_session() as db:
        new_truth = Model.Truth(question=content, rating=rating)
        db.add(new_truth)
        await db.commit()
        await db.refresh(new_truth)
        return new_truth


async def get_random_pg_question() -> Model.Truth:
    db: AsyncSession
    async with get_session() as db:
        query = select(Model.Truth.question).where(Model.Truth.rating == 1)
        result = await db.execute(query)
        return random.choice(result.all())


async def get_random_r_question() -> Model.Truth:
    db: AsyncSession
    async with get_session() as db:
        query = select(Model.Truth.question).where(Model.Truth.rating == 0)
        result = await db.execute(query)
        return random.choice(result.all())


async def create_dare(rating: int, content: str) -> Model.Dare:
    db: AsyncSession
    async with get_session() as db:
        new_dare = Model.Dare(dare=content, rating=rating)
        db.add(new_dare)
        await db.commit()
        await db.refresh(new_dare)
        return new_dare


async def get_random_pg_dare() -> Model.Dare:
    db: AsyncSession
    async with get_session() as db:
        query = select(Model.Dare.dare).where(Model.Dare.rating == 1)
        result = await db.execute(query)
        return random.choice(result.all())


async def get_random_r_dare() -> Model.Dare:
    db: AsyncSession
    async with get_session as db:
        query = select(Model.Dare.dare).where(Model.Dare.rating == 0)
        result = await db.execute(query)
        return random.choice(result.all())
