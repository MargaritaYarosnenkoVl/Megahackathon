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
                        Tuple,
                        )

metadata = MetaData()

tag = Table("tag",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("tag_name", String),  # science, games, auto, sport, show, education, agriculture ...
            )

search_word = Table("search_word",
                    metadata,
                    Column("id", Integer, primary_key=True),
                    Column("word", String),  # any single word
                    )

article = Table("article",
                metadata,
                Column("id", Integer, primary_key=True),
                Column("title", String),  # название
                Column("brief_text", Text),  # короткое описание
                Column("full_text", Text),  # полный текст
                Column("key_words", String),  # 20 key words defined with NLTK and Scikit-Learn (TfidfVectorizer)
                Column("words_for_search", ForeignKey(search_word.c.id)),
                Column("tag", ForeignKey(tag.c.id)),  # тэг - одно слово
                Column("full_text_link", String),  # ссылка на полный текст
                Column("created_at", TIMESTAMP, default=datetime.utcnow()),  # дата публикации
                Column("parsed_at", TIMESTAMP, default=datetime.utcnow()),  # дата добавления / парсинга
                )
