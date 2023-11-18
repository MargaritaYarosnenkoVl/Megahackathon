from pydantic import BaseModel
from datetime import datetime


class News(BaseModel):
    id: int
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
