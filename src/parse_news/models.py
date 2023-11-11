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
                Column("origin_url", String),
                Column("title", String),
                Column("brief_text", Text),
                Column("full_text", Text),
                Column("key_words", String),
                Column("full_text_link", Text),
                Column("created_at", TIMESTAMP, default=datetime.utcnow()),
                Column("parsed_at", TIMESTAMP, default=datetime.utcnow()),
                )
