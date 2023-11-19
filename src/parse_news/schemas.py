from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


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
    tag: str
    search_words: str
    ml_key_words: str
    parsed_from: str
    published_at: datetime
    parsed_at: datetime

    class Config:
        orm_mode = True


class Tag(BaseModel):
    tag: str | None

    class Config:
        orm_mode = True
