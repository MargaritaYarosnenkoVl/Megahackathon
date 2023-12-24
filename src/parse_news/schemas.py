from pydantic import BaseModel, Field, validator
from typing import Optional, Literal, Any
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
    username: str | None
    spidername: str | None

    class Config:
        orm_mode = True


class MainNews(News):

    class Config:
        fields = {"spidername": {"exclude": True}}
        orm_mode = True


class TempNews(News):

    class Config:
        fields = {"spidername": {"exclude": True}}
        orm_mode = True


class NewsID(News):

    class Config:
        fields = {"spidername": {"exclude": True}}
        orm_mode = True



class Tag(BaseModel):
    tag: str | None

    class Config:
        orm_mode = True


class Origin(BaseModel):
    parsed_from: str | None

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


class NewsFilter(BaseModel):
    parsed_from: ParsedFrom = Field(default="cnews.ru", alias="news_origin")
    published_at_high: datetime = Field(default=datetime.utcnow(), alias="date_published_up_to_")
    published_at_low: datetime = Field(default=datetime.utcnow()-timedelta(days=7), alias="date_published_from_")

    class Config:
        orm_mode = True


class SpiderOrigin(BaseModel):
    parsed_from: ParsedFrom = Field(default="naked-science.ru")

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


class Spider(BaseModel):
    name: SpiderName = Field(default="naked_science")

    class Config:
        orm_mode = False


class KeyWord(str):
    name: str


class Count(int):
    quantity: int


class JobID(str):
    scrapyd_job_id: str | None


class UserNameBase(str, Enum):
    admin = "admin"
    user = "user"
    user777 = "user777"
    user77 = "user77"
    bushuev_alex = "bushuev-alex"
    mary = "mary"
    alex = "alex"
    andrey = "andrey"
    test = "test"
    test123 = "test123"
    dima = "dima"
    dima12 = "dima12"
    Aku = "Aku"
    AkuQ = "AkuQ"
    celery = "celery"


class UserName(BaseModel):
    name: UserNameBase = Field(default="alex")

    class Config:
        orm_mode = False


class DeleteNews(BaseModel):
    rowcount: int | Any
    _soft_closed: bool | Any

    class Config:
        orm_mode = True
