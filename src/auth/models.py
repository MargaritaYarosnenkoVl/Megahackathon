import bcrypt
from datetime import datetime
from typing import AsyncGenerator

from fastadmin import register, SqlAlchemyModelAdmin
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import String, Boolean, Column, Integer, TIMESTAMP, ForeignKey, select, MetaData, Table, JSON
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped

from ..database import Base, DATABASE_URL, async_session_maker

metadata = MetaData()


role = Table("role",
             metadata,
             Column("id", Integer, primary_key=True),
             Column("name", String, nullable=False),
             Column("permissions", JSON)
             )


user = Table("user",
             metadata,
             Column("id", Integer, primary_key=True),
             Column("username", String, nullable=False),
             Column("hashed_password", String(length=1024), nullable=False),
             Column("registred_at", TIMESTAMP, default=datetime.utcnow),
             Column("role_id", Integer, ForeignKey(role.c.id)),
             Column("email", String(length=320), unique=True, index=True, nullable=False),
             Column("is_active", Boolean, default=True, nullable=False),
             Column("is_superuser", Boolean, default=False, nullable=False),
             Column("is_verified", Boolean, default=False, nullable=False)
             )


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
    yield SQLAlchemyUserDatabase(session, User)
    