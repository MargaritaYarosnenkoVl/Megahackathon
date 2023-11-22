import json
import os
from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.parse_news.models import article
from src.parse_news.parse_news.spiders.naked_science_launcher import SpiderFromCode
from .schemas import News, FilterNews, Tag, Origin, NewsJSONNoID, SpiderName
from typing import List

router = APIRouter(prefix="/get",
                   tags=["Get News"])

launch_parser = APIRouter(prefix="/launch",
                          tags=["Launch parser"])


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


@router.get("/tags/unique", response_model=List[Tag])  # response_model=OfferSearchResult, operation_id="offer_search"
async def get_unique_tags(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(article.c.tag).distinct()
        result = await session.execute(query)
        return result.all()
    except:
        return {"status": "error",
                "data": None,
                "details": None}


@router.get("/origins/unique", response_model=List[Origin])  # response_model=OfferSearchResult, operation_id="offer_search"
async def get_unique_origins(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(article.c.parsed_from).distinct()
        result = await session.execute(query)
        return result.all()
    except:
        return {"status": "error",
                "data": None,
                "details": None}


@router.post("/filter", response_model=List[News])  # response_model=OfferSearchResult, operation_id="offer_search"
async def filter_news(data: FilterNews, session: AsyncSession = Depends(get_async_session)):
    tag = data.tag
    search_words = data.search_words
    ml_key_words = data.ml_key_words
    parsed_from = data.parsed_from
    published_at = data.published_at
    parsed_at = data.parsed_at
    try:
        query = select(article).where(or_(article.c.tag == tag,
                                      # article.c.search_words == search_words,
                                      # article.c.ml_key_words == ml_key_words,
                                      article.c.parsed_from == parsed_from,
                                      article.c.published_at <= published_at,
                                      article.c.parsed_at <= parsed_at
                                      ))
        print(query.params())
        result = await session.execute(query)
        return result.all()
    except:
        return {"status": "error",
                "data": None,
                "details": None}


@launch_parser.get("/{naked_science}")  # , response_model=List[NewsJSONNoID]
async def launch_naked_science(spider_name: SpiderName, session: AsyncSession = Depends(get_async_session)):
    try:
        # return None
        s = SpiderFromCode(spider_name)
        s.parse()
        # s.stop()
    except Exception as e:
        print(e)
        return {"status": "error",
                "data": e,
                "details": e}
    finally:
        with open(f"src/parse_news/parse_news/spiders/json_data/{spider_name}.json", "r") as f:
            data = f.read()
        return json.loads(data)

#
# if __name__ == "__main__":
#     get_news_by_id()
