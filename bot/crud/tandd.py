import random

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

import models.tandd as Model


async def create_truth(db: AsyncSession, rating: int, content: str) -> Model.Truth:
    new_truth = Model.Truth(question=content, rating=rating)
    db.add(new_truth)
    await db.commit()
    await db.refresh(new_truth)
    return new_truth


async def get_random_pg_question(db: AsyncSession) -> str:
    query = select(Model.Truth.question).where(Model.Truth.rating == 1)
    result = await db.execute(query)
    return random.choice(result.all())


async def get_random_r_question(db: AsyncSession) -> str:
    query = select(Model.Truth.question).where(Model.Truth.rating == 0)
    result = await db.execute(query)
    return random.choice(result.all())


async def create_dare(db: AsyncSession, rating: int, content: str) -> Model.Dare:
    new_dare = Model.Dare(dare=content, rating=rating)
    db.add(new_dare)
    await db.commit()
    await db.refresh(new_dare)
    return new_dare


async def get_random_pg_dare(db: AsyncSession) -> str:
    query = select(Model.Dare.dare).where(Model.Dare.rating == 1)
    result = await db.execute(query)
    return random.choice(result.all())


async def get_random_r_dare(db: AsyncSession) -> str:
    query = select(Model.Dare.dare).where(Model.Dare.rating == 0)
    result = await db.execute(query)
    result_list = result.all()
    return random.choice(result_list)
