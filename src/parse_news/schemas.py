from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
from datetime import datetime, timedelta
from enum import Enum


class News(BaseModel):
    id: Optional[int] = Field(1, ge=1)
    title: str
    brief_text: str | None
    full_text: str
    tag: str | None
    search_words: str | None
    ml_key_words: str | None
    parsed_from: str
    full_text_link: str
    published_at: datetime
    parsed_at: datetime
    rating: int | None
    counter: int | None
    fun_metric: float | None
    unique_metric: float | None
    simple_metric: float | None

    class Config:
        orm_mode = True


class ParsedFrom(str, Enum):
    naked_science = "naked-science.ru"
    cnews = "cnews.ru"
    fontanka = "fontanka.ru"
    dimonvideo = "dimonvideo.ru"
    news3d = "3dnews.ru"
    forbes = "forbes.ru"
    knife_media = "knife.media"
    nplus1 = "nplus1.ru"
    portal_kultura = "portal-kultura.ru"
    sdelanounas = "sdelanounas.ru"
    snob = "snob.ru"
    techno_news = "techno-news.ru"
    windozo = "windozo.ru"


class FilterNews(BaseModel):
    # tag: str = Field(default="наука", alias="Тема новости")
    # search_words: str = Field(alias="Поиск по темам/тэгам")
    # ml_key_words: str = Field(alias="Ключевые слова")
    parsed_from: ParsedFrom = Field(default="cnews.ru", alias="Источник новости")
    published_at_high: datetime = Field(default=datetime.utcnow(), alias="Дата публикации до")
    published_at_low: datetime = Field(default=datetime.utcnow()-timedelta(days=7), alias="Дата публикации с")

    class Config:
        orm_mode = True


class Tag(BaseModel):
    tag: str | None

    class Config:
        orm_mode = True


class Origin(BaseModel):
    parsed_from: str | None

    class Config:
        orm_mode = True


class NewsJSONNoID(BaseModel):
    title: str
    brief_text: str
    full_text: str
    tag: str | None
    search_words: str | None
    ml_key_words: str | None
    parsed_from: str
    full_text_link: str
    published_at: datetime
    parsed_at: datetime
    rating: int | None
    counter: int | None
    fun_metric: float | None
    unique_metric: float | None
    simple_metric: float | None

    class Config:
        orm_mode = True


class SpiderName(str, Enum):
    naked_science = "naked_science"
    cnews = "cnews"
    fontanka = "fontanka"
    dimonvideo = "dimonvideo"
    news3d = "news3d"
    forbes = "forbes"
    knife_media = "knife_media"
    nplus1 = "nplus1"
    portal_kultura = "portal_kultura"
    sdelanounas = "sdelanounas"
    snob = "snob"
    techno_news = "techno_news"
    windozo = "windozo"


class KeyWord(str):
    name: str


class Count(int):
    quantity: int
