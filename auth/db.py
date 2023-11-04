from datetime import datetime
from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import String, Boolean, Column, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from config import FSTR_DB_HOST, FSTR_DB_PORT, FSTR_DB_LOGIN, FSTR_DB_PASS, DB_NAME
from models.models import role

DATABASE_URL = f"postgresql+asyncpg://{FSTR_DB_LOGIN}:{FSTR_DB_PASS}@{FSTR_DB_HOST}:{FSTR_DB_PORT}/{DB_NAME}"


class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column("id", Integer, primary_key=True)
    username = Column("username", String, nullable=False)
    hashed_password: Mapped[str] = Column(String(length=1024), nullable=False)
    registred_at = Column("registred_at", TIMESTAMP, default=datetime.utcnow)
    role_id = Column("role_id", Integer, ForeignKey(role.c.id))
    email: Mapped[str] = Column(String(length=320), unique=True, index=True, nullable=False)
    is_active: Mapped[bool] = Column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = Column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = Column(Boolean, default=False, nullable=False)


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


# async def create_db_and_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
    