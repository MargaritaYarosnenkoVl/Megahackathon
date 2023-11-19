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
    tag: str = Field(default="science")
    search_words: str = Field()
    ml_key_words: str = Field()
    parsed_from: str = Field(default="Нож")
    published_at: datetime = Field(default=datetime.fromisoformat("2023-11-01T00:00:00.000"))
    parsed_at: datetime = Field(default=datetime.fromisoformat("2023-11-01T00:00:00.000"))

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