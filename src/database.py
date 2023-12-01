from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
from config import FSTR_DB_HOST, FSTR_DB_PORT, FSTR_DB_LOGIN, FSTR_DB_PASS, FSTR_DB_NAME

DATABASE_URL = f"postgresql+asyncpg://{FSTR_DB_LOGIN}:{FSTR_DB_PASS}@{FSTR_DB_HOST}:{FSTR_DB_PORT}/{FSTR_DB_NAME}"

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

metadata = MetaData()


class Base(DeclarativeBase):
    metadata = metadata


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
