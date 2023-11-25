import json
import os
import subprocess
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, and_, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from scrapy.crawler import CrawlerProcess
from src.database import get_async_session
from src.parse_news.models import article
from src.parse_news.parse_news.spiders.spider_launcher import SpiderFromCode
from src.tokenizer.tokenize_from_db import main as main_tokenizer
from .schemas import News, FilterNews, Tag, Origin, NewsJSONNoID, SpiderName, KeyWord, Count
from typing import List, Literal

# from src.parse_news.parse_news.pipelines import ParseNewsPipeline

get_router = APIRouter(prefix="/get",
                       tags=["Get News"])

launch_parser_router = APIRouter(prefix="/launch",
                                 tags=["Launch parser"])


@get_router.get("/count/all", response_model=Count)  # response_model=OfferSearchResult, operation_id="offer_search"
async def whole_quantity(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(func.count(article.c.id))
        result = await session.execute(query)
        return result.scalar()
    except Exception as e:
        print(e)
        return {"status": "error",
                "data": e,
                "details": e}


@get_router.get("/single/{item_id}",
                response_model=List[News])  # response_model=OfferSearchResult, operation_id="offer_search"
async def get_news_by_id(item_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(article).where(article.c.id == item_id)
        result = await session.execute(query)
        return result.all()
    except Exception as e:
        print(e)
        return {"status": "error",
                "data": e,
                "details": e}


@get_router.get("/many/{last_n}", response_model=List[News])
async def get_last_published(last_n: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(article).order_by(article.c.published_at.desc()).limit(last_n)
        result = await session.execute(query)
        return result.all()
    except Exception as e:
        print(e)
        return {"status": "error",
                "data": e,
                "details": e}


@get_router.get("/tags/unique",
                response_model=List[Tag])  # response_model=OfferSearchResult, operation_id="offer_search"
async def get_unique_tags(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(article.c.tag).distinct()
        result = await session.execute(query)
        return result.all()
    except Exception as e:
        print(e)
        return {"status": "error",
                "data": e,
                "details": e}


@get_router.get("/origins/unique", response_model=List[Origin])
                                        # response_model=OfferSearchResult, operation_id="offer_search"
async def get_unique_origins(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(article.c.parsed_from).distinct()
        result = await session.execute(query)
        return result.all()
    except Exception as e:
        print(e)
        return {"status": "error",
                "data": e,
                "details": e}



@get_router.post("/filter", response_model=List[News])  # response_model=OfferSearchResult, operation_id="offer_search"
async def filter_news(data: FilterNews, session: AsyncSession = Depends(get_async_session)):
    tag = data.tag
    search_words = data.search_words
    ml_key_words = data.ml_key_words
    parsed_from = data.parsed_from
    published_at = datetime.strptime(data.published_at, "")
    parsed_at = datetime.strptime(data.parsed_at)
    try:
        query = select(article).where(or_(article.c.tag == tag,
                                          # article.c.search_words == search_words,
                                          # article.c.ml_key_words == ml_key_words,
                                          article.c.parsed_from == parsed_from,
                                          article.c.published_at <= published_at,
                                          article.c.parsed_at <= parsed_at
                                          ))
        result = await session.execute(query)
        return result.all()
    except Exception as e:
        print(e)
        return {"status": "error",
                "data": e,
                "details": e}


@get_router.get("/filter_kw/{key_word}", response_model=List[News])
async def filter_news_by_key_word(key_word: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(article).where(article.c.ml_key_words.ilike(f"%{key_word}%")).order_by(
            article.c.published_at.desc())
        result = await session.execute(query)
        return result.all()
    except Exception as e:
        return {"status": "error",
                "data": e,
                "details": e}


@get_router.get("/filter_t/{tag}", response_model=List[News])
async def filter_news_by_tag(tag: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(article).where(article.c.tag.ilike(f"%{tag}%")).order_by(article.c.published_at.desc())
        result = await session.execute(query)
        return result.all()
    except Exception as e:
        return {"status": "error",
                "data": e,
                "details": e}


@launch_parser_router.get("/{spider_name}")
async def launch_spider(spider_name: SpiderName, session: AsyncSession = Depends(get_async_session)):
    try:
        subprocess.call(["spider_launcher.sh", "spider_launcher.py", "$PATH"],
                         env={"PATH": "/home/alexander/PycharmProjects/Megahackathon_T17/src/parse_news/parse_news/spiders"})
        print("OK")
        # spider = SpiderFromCode(spider_name)
        # spider.parse()
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
        # with open(f"src/parse_news/parse_news/spiders/json_data/{spider_name}.json", "r") as f:
        #     data = f.read()
        # return json.loads(data)
    except Exception as e:
        print(e)
        return {"status": "error",
                "data": e,
                "details": e}
    finally:
        # with open(f"src/parse_news/parse_news/spiders/json_data/{spider_name}.json", "r") as f:
        #     data = f.read()
        # return json.loads(data)
         return "Coming soon"




@get_router.get("/ml_key_words}")
async def fill_ml_key_words(session: AsyncSession = Depends(get_async_session)):
    try:
        pass
    except Exception as e:
        print(e)
        return {"status": "error",
                "data": e,
                "details": e}
    finally:
        # with open(f"src/parse_news/parse_news/spiders/json_data/{spider_name}.json", "r") as f:
        #     data = f.read()
        # return json.loads(data)
         return "Coming soon"


#
# if __name__ == "__main__":
#     get_news_by_id()
