import json
import os
from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from scrapy.crawler import CrawlerProcess
from src.database import get_async_session
from src.parse_news.models import article
# from src.parse_news.parse_news.spiders.naked_science_spider_CLI import NakedScienceSpider
from .schemas import News, FilterNews, Tag, Origin, NewsJSONNoID, SpiderName
from typing import List
# from src.parse_news.parse_news.pipelines import ParseNewsPipeline

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


@router.get("/origins/unique",
            response_model=List[Origin])  # response_model=OfferSearchResult, operation_id="offer_search"
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


@launch_parser.get("/{spider_name}")
async def launch_spider(spider_name: SpiderName, session: AsyncSession = Depends(get_async_session)):
    try:
        # s = SpiderFromCode(spider_name)
        # spider = s.get_spider_by_name()
        # settings = {"FEEDS": {f"src/parse_news/parse_news/spiders/json_data/{spider_name}.json": {"format": "json",
        #                                                                                           "overwrite": True}
        #                       },
        #             "ITEM_PIPELINES": {ParseNewsPipeline: 300}}
        # process = CrawlerProcess(settings=settings)
        # res = await process.crawl(NakedScienceSpider).addBoth()
        # process.start()
        # await process.stop()
        # return None
        # s = SpiderFromCode(spider_name)
        # s.parse()
        # s.stop()
        with open(f"src/parse_news/parse_news/spiders/json_data/{spider_name}.json", "r") as f:
            data = f.read()
        return json.loads(data)
    except Exception as e:
        print(e)
        return {"status": "error",
                "data": e,
                "details": e}
    finally:
        return "Coming soon"


#
# if __name__ == "__main__":
#     get_news_by_id()
