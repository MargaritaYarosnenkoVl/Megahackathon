from datetime import datetime
from typing import Optional
import sqlalchemy

from sqlalchemy import (MetaData,
                        Table,
                        Column,
                        Integer,
                        Float,
                        String,
                        TIMESTAMP,
                        ForeignKey,
                        JSON,
                        Boolean,
                        Text,
                        Tuple,
                        )

metadata = MetaData()

article = Table("article",
                metadata,
                Column("id", Integer, primary_key=True, autoincrement="auto"),
                Column("title", Text),  # название
                Column("brief_text", Text),  # короткое описание
                Column("full_text", Text),  # полный текст
                Column("tag", String),  # тэг - тема новости (первое слово/фраза из группы тегов)
                Column("search_words", Text),  # строка всех тегов
                Column("ml_key_words", Text),  # 20 ключевых слов выдел с помощью NLTK and Scikit-Learn
                Column("parsed_from", String),  # название сайта
                Column("full_text_link", Text),  # ссылка на полный текст
                Column("published_at", TIMESTAMP, default=datetime.utcnow()),  # дата публикации
                Column("parsed_at", TIMESTAMP, default=datetime.utcnow()),  # дата добавления / парсинга
                Column("rating", Integer, default=0),  # рейтинг новости, каждый вывод в поиске +1
                Column("counter", Integer, default=0),  # сколько раз встречалась на сайтах
                Column("fun_metric", Float, default=0),  # метрика забавности что ли
                Column("unique_metric", Float, default=0),  # метрика уникальности
                Column("simple_metric", Float, default=0)  # метрика простоты понимания
                )

temp_article = Table("temp_article",
                     metadata,
                     Column("id", Integer, primary_key=True, autoincrement="auto"),
                     Column("title", Text),  # название
                     Column("brief_text", Text),  # короткое описание
                     Column("full_text", Text),  # полный текст
                     Column("tag", String),  # тэг - тема новости (первое слово/фраза из группы тегов)
                     Column("search_words", Text),  # строка всех тегов
                     Column("ml_key_words", Text),  # 20 ключевых слов выдел с помощью NLTK and Scikit-Learn
                     Column("parsed_from", String),  # название сайта
                     Column("full_text_link", Text),  # ссылка на полный текст
                     Column("published_at", TIMESTAMP, default=datetime.utcnow()),  # дата публикации
                     Column("parsed_at", TIMESTAMP, default=datetime.utcnow()),  # дата добавления / парсинга
                     Column("rating", Integer, default=0),  # рейтинг новости, каждый вывод в поиске +1
                     Column("counter", Integer, default=0),  # сколько раз встречалась на сайтах
                     Column("fun_metric", Float, default=0),  # метрика забавности что ли
                     Column("unique_metric", Float, default=0),  # метрика уникальности
                     Column("simple_metric", Float, default=0),  # метрика простоты понимания
                     Column("username", String),
                     Column("spidername", String),
                     )
