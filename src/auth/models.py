import bcrypt
from datetime import datetime
from typing import AsyncGenerator, List

from fastadmin import register, SqlAlchemyModelAdmin
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTable, SQLAlchemyBaseOAuthAccountTable
from sqlalchemy import String, Boolean, Column, Integer, TIMESTAMP, ForeignKey, select, MetaData, Table, JSON
from sqlalchemy.ext.asyncio import AsyncSession  # async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, relationship, mapped_column

from database import Base, async_session_maker  # DATABASE_URL,

metadata = MetaData()


class Role(Base):
    metadata = metadata
    __tablename__ = "role"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True, primary_key=True)


class User(SQLAlchemyBaseUserTable[int], Base):
    metadata = metadata
    __tablename__ = "user"
    # oauth_accounts: Mapped[List[OAuthAccount]] = relationship("OAuthAccount", lazy="joined")
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str | None] = mapped_column(String, default="Иванов Иван Иванович", nullable=False)
    phone_number: Mapped[str | None] = mapped_column(String, default="9871234567")
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    registred_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    role_name: Mapped[str] = mapped_column(String, ForeignKey(Role.name))
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    def __str__(self):
        return self.username


@register(User, sqlalchemy_sessionmaker=async_session_maker)
class UserAdmin(SqlAlchemyModelAdmin):
    exclude = ("hash_password",)
    list_display = ("id", "username", "role_id", "is_superuser", "is_active")
    list_display_links = ("id", "username", "role_id")
    list_filter = ("id", "username", "role_id", "is_superuser", "is_active")
    search_fields = ("username", "role_id", )

    async def authenticate(self, username, password):
        sessionmaker = self.get_sessionmaker()
        async with sessionmaker() as session:
            query = select(User).filter_by(username=username, is_superuser=True)
            result = await session.scalars(query)
            user = result.first()
            if not user:
                return None
            if not bcrypt.checkpw(password.encode(), user.hashed_password.encode()):
                return None
            return user.id

# async def create_db_and_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)  # , OAuthAccount
    