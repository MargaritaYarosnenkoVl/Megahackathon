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
                        Boolean,
                        Text,
                        Tuple)

metadata = MetaData()

article = Table("article",
                metadata,
                Column("id", Integer, primary_key=True),
                Column("title", String),
                Column("text", Text),
                Column("key_words", String),
                Column("timedata", TIMESTAMP),
                )
