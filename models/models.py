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
             Column("email", String, nullable=False),
             Column("username", String, nullable=False),
             Column("password", String, nullable=False),
             Column("registred_at", TIMESTAMP, default=datetime.utcnow),
             Column("role_id", Integer, ForeignKey(role.c.id))
             )
