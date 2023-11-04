from datetime import datetime
from typing import Optional

import sqlalchemy
from sqlalchemy import (MetaData,
                        Table,
                        Column,
                        Integer,
                        String,
                        TIMESTAMP,
                        ForeignKey,
                        JSON,
                        Boolean)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

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
