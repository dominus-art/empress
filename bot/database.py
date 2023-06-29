from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from config import get_settings


engine = create_async_engine(
    get_settings().SQLITE_URI,
    future=True,
    echo=True,
    connect_args={"check_same_thread": False},
)

async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_session():
    async with async_session() as sess:
        async with sess.begin():
            try:
                yield sess
            except:
                await sess.rollback()
            finally:
                await sess.close()
