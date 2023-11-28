import bcrypt
from datetime import datetime
from typing import AsyncGenerator, List

from fastadmin import register, SqlAlchemyModelAdmin
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTable, SQLAlchemyBaseOAuthAccountTable
from sqlalchemy import String, Boolean, Column, Integer, TIMESTAMP, ForeignKey, select, MetaData, Table, JSON
from sqlalchemy.ext.asyncio import AsyncSession  # async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, relationship  # DeclarativeBase,

from database import Base, async_session_maker  # DATABASE_URL,

metadata = MetaData()


role = Table("role",
             metadata,
             Column("id", Integer, primary_key=True),
             Column("name", String, nullable=False),
             # Column("permissions", JSON)
             )


user = Table("user",
             metadata,
             Column("id", Integer, primary_key=True),
             Column("full_name", String, default="Иванов Иван Иванович"),
             Column("phone_number", String, default="9871234567"),
             Column("username", String, nullable=False, unique=True),
             Column("hashed_password", String(length=1024), nullable=False),
             Column("registred_at", TIMESTAMP, default=datetime.utcnow),
             Column("role_id", Integer, ForeignKey(role.c.id)),
             Column("email", String(length=320), unique=True, index=True, nullable=False),
             Column("is_active", Boolean, default=True, nullable=False),
             Column("is_superuser", Boolean, default=False, nullable=False),
             Column("is_verified", Boolean, default=False, nullable=False)
             )

#
# class OAuthAccount(SQLAlchemyBaseOAuthAccountTable[int], Base):
#     id = Column(Integer, primary_key=True)
#
#     @declared_attr
#     def user_id(cls):
#         return Column(Integer, ForeignKey("user.id", ondelete="cascade"), nullable=False)


class User(SQLAlchemyBaseUserTable[int], Base):
    # oauth_accounts: Mapped[List[OAuthAccount]] = relationship("OAuthAccount", lazy="joined")
    id = Column("id", Integer, primary_key=True)
    full_name = Column("full_name", String, default="Иванов Иван Иванович", nullable=False)
    phone_number = Column("phone_number", String, default="9871234567")
    username = Column("username", String, nullable=False, unique=True)
    hashed_password = Column(String(length=1024), nullable=False)
    registred_at = Column("registred_at", TIMESTAMP, default=datetime.utcnow)
    role_id = Column("role_id", Integer, ForeignKey(role.c.id))
    email = Column(String(length=320), unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

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
    