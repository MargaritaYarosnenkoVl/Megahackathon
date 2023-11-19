from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.parse_news.models import article
from src.parse_news.parse_news.spiders import naked_science_spider
from .schemas import News, FilterNews, Tag
from typing import List

router = APIRouter(prefix="/get",
                   tags=["Get News"])


@router.get("/{item_id}", response_model=List[News])  # response_model=OfferSearchResult, operation_id="offer_search"
async def get_news_by_id(item_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(article).where(article.c.id == item_id)
        result = await session.execute(query)
        return result.all()
    except:
        return {"status": "error",
                "data": None,
                "details": None}


@router.get("/tags/all_unique", response_model=List[Tag])  # response_model=OfferSearchResult, operation_id="offer_search"
async def get_unique_tags(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(article.c.tag).distinct()
        result = await session.execute(query)
        return result.all()
    except:
        return {"status": "error",
                "data": None,
                "details": None}


@router.post("/filter/", response_model=List[News])  # response_model=OfferSearchResult, operation_id="offer_search"
async def filter_news(data: FilterNews, session: AsyncSession = Depends(get_async_session)):
    tag = data.tag
    search_words = data.search_words
    ml_key_words = data.ml_key_words
    parsed_from = data.parsed_from
    published_at = data.published_at
    parsed_at = data.parsed_at
    try:
        query = select(article).where(or_(article.c.tag == tag,
                                      article.c.search_words == search_words,
                                      article.c.ml_key_words == ml_key_words,
                                      article.c.parsed_from == parsed_from,
                                      article.c.published_at >= published_at,
                                      article.c.parsed_at >= parsed_at
                                      ))
        print(query.params())
        result = await session.execute(query)
        return result.all()
    except:
        return {"status": "error",
                "data": None,
                "details": None}


if __name__ == "__main__":
    get_news_by_id()
