from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.parse_news.models import article
from src.parse_news.parse_news.spiders import naked_science_spider
from .schemas import News
from typing import List

router = APIRouter(prefix="/get_news_by_id",
                   tags=["Get news"])


@router.get("/{item_id}", response_model=List[News])  # response_model=OfferSearchResult, operation_id="offer_search"
async def get_news_by_id(item_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        # query = session.get(article, item_id)
        query = article.select().where(article.c.id == item_id)
        result = await session.execute(query)
        return result.all()
    except:
        return {"ststus": "error",
                "data": None,
                "details": None}


if __name__ == "__main__":
    get_news_by_id()
