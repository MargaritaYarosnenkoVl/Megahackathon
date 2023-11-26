import subprocess
import sys
import json
from typing import List
from fastapi import APIRouter, Depends

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from tokenizer.tokenize_from_db import main as main_tokenizer
from .models import article
from .schemas import News, FilterNews, Tag, Origin, SpiderName, Count, JobID

get_router = APIRouter(prefix="/get",
                       tags=["Get News"])

schedule_parser_router = APIRouter(prefix="/launch",
                                   tags=["Schedule parser"])

fill_ml = APIRouter(prefix="/launch",
                    tags=["Fill key words with tokenizer"])


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
    try:
        query = select(article).filter(article.c.parsed_from == data.parsed_from,
                                       article.c.published_at >= data.published_at_low,
                                       article.c.published_at <= data.published_at_high
                                       ).order_by(article.c.published_at.desc())
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


@schedule_parser_router.get("/{spider_name}", response_model=JobID)
async def launch_spider(spider_name: SpiderName, session: AsyncSession = Depends(get_async_session)):
    try:
        result = subprocess.run([f"curl",
                                 f"http://localhost:6800/schedule.json",
                                 f"-d",
                                 f"project=parse_news",
                                 f"-d",
                                 f"spider={spider_name}"],
                                stdout=subprocess.PIPE)
        print("OK")
        return json.loads(result.stdout)["jobid"]  # ' '.join(sys.argv[1:])  # "Spider is running. Please, weight."
    except Exception as e:
        print(e)
        return {"status": "error",
                "data": e,
                "details": e}
    finally:
        # with open(f"src/parse_news/parse_news/spiders/json_data/{spider_name}.json", "r") as f:
        #     data = f.read()
        # return json.loads(data)
        # return "Coming soon"
        pass


@fill_ml.get("/ml_key_words")
async def fill_ml_key_words(session: AsyncSession = Depends(get_async_session)):
    try:
        main_tokenizer()
    except Exception as e:
        print(e)
        return {"status": "error",
                "data": e,
                "details": e
                }
    finally:
        # with open(f"src/parse_news/parse_news/spiders/json_data/{spider_name}.json", "r") as f:
        #     data = f.read()
        # return json.loads(data)
        return "Coming soon"

#
# if __name__ == "__main__":
#     get_news_by_id()
