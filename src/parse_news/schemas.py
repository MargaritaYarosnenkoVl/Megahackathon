from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
from datetime import datetime
from enum import Enum


class News(BaseModel):
    id: Optional[int] = Field(1, ge=1)
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


class FilterNews(BaseModel):
    tag: str = Field(default="наука", alias="Тема новости")
    search_words: str = Field(alias="Поиск по темам/тэгам")
    ml_key_words: str = Field(alias="Ключевые слова")
    parsed_from: str = Field(default="cnews.ru", alias="Источник новости")
    published_at: datetime = Field(default=datetime.fromisoformat("2023-11-01T00:00:00.000"), alias="Дата публикации")
    parsed_at: datetime = Field(default=datetime.fromisoformat("2023-11-01T00:00:00.000"), alias="Дата парсинга")

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


class SpiderNameCls(str, Enum):
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


class SpiderName(BaseModel):
    name: list[SpiderNameCls]

    # @validator('c')
    # def c_match(self, v):
    #     if not v in ['naked_science', 'cnews']:
    #         raise ValueError('c must be in [naked_science, cnews]')
    #     return v


class KeyWord(str):
    name: str


class Count(int):
    quantity: int = Field()
