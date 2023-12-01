from datetime import datetime
from sqlalchemy import (MetaData, Table, Column, Integer, Float, String, TIMESTAMP, Text)
from sqlalchemy.orm import Mapped, relationship, mapped_column
from database import Base

metadata = MetaData()


class Article(Base):
    metadata = metadata
    __tablename__ = "article"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement="auto")
    title: Mapped[str | None] = mapped_column(Text)  # название
    brief_text: Mapped[str | None] = mapped_column(Text)  # короткое описание
    full_text: Mapped[str | None] = mapped_column(Text)  # полный текст
    tag: Mapped[str | None] = mapped_column(String)  # тэг - тема новости (первое слово/фраза из группы тегов)
    search_words: Mapped[str | None] = mapped_column(Text)  # строка всех тегов
    ml_key_words: Mapped[str | None] = mapped_column(Text)  # 20 ключевых слов выдел с помощью NLTK and Scikit-Learn
    parsed_from: Mapped[str | None] = mapped_column(String)  # название сайта
    full_text_link: Mapped[str | None] = mapped_column(Text)  # ссылка на полный текст
    published_at: Mapped[TIMESTAMP | None] = mapped_column(TIMESTAMP, default=datetime.utcnow())  # дата публикации
    parsed_at: Mapped[TIMESTAMP | None] = mapped_column(TIMESTAMP, default=datetime.utcnow())  # дата добавления / парсинга
    rating: Mapped[int | None] = mapped_column(Integer, default=0)  # рейтинг новости, каждый вывод в поиске +1
    counter: Mapped[int | None] = mapped_column(Integer, default=0)  # сколько раз встречалась на сайтах
    fun_metric: Mapped[float | None] = mapped_column(Float, default=0)  # метрика забавности что ли
    unique_metric: Mapped[float | None] = mapped_column(Float, default=0)  # метрика уникальности
    simple_metric: Mapped[float | None] = mapped_column(Float, default=0)  # метрика простоты понимания
    username: Mapped[str | None] = mapped_column(String)  # кто добавил


class TempArticle(Base):
    metadata = metadata
    __tablename__ = "temp_article"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement="auto")
    title: Mapped[str | None] = mapped_column(Text)  # название
    brief_text: Mapped[str | None] = mapped_column(Text)  # короткое описание
    full_text: Mapped[str | None] = mapped_column(Text)  # полный текст
    tag: Mapped[str | None] = mapped_column(String)  # тэг - тема новости (первое слово/фраза из группы тегов)
    search_words: Mapped[str | None] = mapped_column(Text)  # строка всех тегов
    ml_key_words: Mapped[str | None] = mapped_column(Text)  # 20 ключевых слов выдел с помощью NLTK and Scikit-Learn
    parsed_from: Mapped[str | None] = mapped_column(String)  # название сайта
    full_text_link: Mapped[str | None] = mapped_column(Text)  # ссылка на полный текст
    published_at: Mapped[TIMESTAMP | None] = mapped_column(TIMESTAMP, default=datetime.utcnow())  # дата публикации
    parsed_at: Mapped[TIMESTAMP | None] = mapped_column(TIMESTAMP, default=datetime.utcnow())  # дата добавления / парсинга
    rating: Mapped[int | None] = mapped_column(Integer, default=0)  # рейтинг новости, каждый вывод в поиске +1
    counter: Mapped[int | None] = mapped_column(Integer, default=0)  # сколько раз встречалась на сайтах
    fun_metric: Mapped[float | None] = mapped_column(Float, default=0)  # метрика забавности что ли
    unique_metric: Mapped[float | None] = mapped_column(Float, default=0)  # метрика уникальности
    simple_metric: Mapped[float | None] = mapped_column(Float, default=0)  # метрика простоты понимания
    username: Mapped[str | None] = mapped_column(String)  # кто добавил
    spidername: Mapped[str | None] = mapped_column(String)  # названия спайдера
