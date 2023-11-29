import subprocess
import sys
import json
import time
from typing import List
from fastapi import APIRouter, Depends

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from tokenizer.tokenize_from_db import main as main_tokenizer
from .models import article, temp_article
from .schemas import (News,
                      FilterNews,
                      Tag,
                      Origin,
                      SpiderName,
                      Count,
                      JobID,
                      TempNews,
                      UserName,
                      UserNameBase,
                      Spider,
                      TempOrigin)

from .schemas import ParsedFrom

get_base_router = APIRouter(prefix="/get",
                            tags=["Get News"])

get_temp_router = APIRouter(prefix="/get",
                            tags=["Get Temp News"])

schedule_parser_router = APIRouter(prefix="/schedule",
                                   tags=["Schedule parser"])


@get_base_router.get("/count/all",
                     response_model=Count)  # response_model=OfferSearchResult, operation_id="offer_search"
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


@get_base_router.get("/single/{item_id}",
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


@get_base_router.get("/many/{last_n}", response_model=List[News])
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


@get_base_router.get("/tags/unique",
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


@get_base_router.get("/origins/unique", response_model=List[Origin])
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


@get_base_router.post("/filter",
                      response_model=List[News])  # response_model=OfferSearchResult, operation_id="offer_search"
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


@get_base_router.get("/filter_kw/{key_word}", response_model=List[News])
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


@get_base_router.get("/filter_t/{tag}", response_model=List[News])
async def filter_news_by_tag(tag: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(article).where(article.c.tag.ilike(f"%{tag}%")).order_by(article.c.published_at.desc())
        result = await session.execute(query)
        return result.all()
    except Exception as e:
        return {"status": "error",
                "data": e,
                "details": e}


@schedule_parser_router.post("/spider", response_model=JobID)  # , response_model=List[TempNews]  ,
async def launch_spider(origin: TempOrigin, username: UserName):
    # origin_spiders = {"naked-science.ru": "naked_science",
    #                   "cnews.ru": "cnews",
    #                   "fontanka.ru": "fontanka",
    #                   "dimonvideo.ru": "dimonvideo",
    #                   "3dnews.ru": "news3d",
    #                   "forbes.ru": "forbes",
    #                   "knife.media": "knife_media",
    #                   "nplus1.ru": "nplus1",
    #                   "portal-kultura.ru": "portal_kultura",
    #                   "sdelanounas.ru": "sdelanounas",
    #                   "snob.ru": "snob",
    #                   "techno-news.ru": "techno_news",
    #                   "windozo.ru": "windozo"}
    # spidername = origin_spiders.get(origin.__dict__.get("parsed_from").__dict__.get("_value_"))
    spidername = origin.__dict__.get("parsed_from").__dict__.get("_name_")
    try:
        proc_result = subprocess.run([f"curl",
                                      f"http://localhost:6800/schedule.json",
                                      f"-d",
                                      f"project=parse_news",
                                      f"-d",
                                      f"spider={spidername}",
                                      f"-d",
                                      f"username={username.name}",
                                      f"-d",
                                      f"spidername={spidername}",
                                      ], stdout=subprocess.PIPE,
                                     cwd="/home/alexander/PycharmProjects/Megahackathon_T17/src/parse_news/parse_news")
        result = json.loads(proc_result.stdout)["jobid"]
        print("OK", "Please, wait while parser is working. JobID: ", result)
        return result
    except Exception as e:
        print(e)
        return {"status": "error",
                "data": e,
                "details": e}


@schedule_parser_router.post("/spider/stop", response_model=JobID)  # , response_model=List[TempNews]  , ,
async def stop_spider(job_id: str):
    try:
        proc_result1 = subprocess.run([f"curl",
                                       f"http://localhost:6800/cancel.json",
                                       f"-d",
                                       f"project=parse_news",
                                       f"-d",
                                       f"job={job_id}"], stdout=subprocess.PIPE,
                                      cwd="/home/alexander/PycharmProjects/Megahackathon_T17/src/parse_news/parse_news")
        proc_result2 = subprocess.run([f"curl",
                                       f"http://localhost:6800/cancel.json",
                                       f"-d",
                                       f"project=parse_news",
                                       f"-d",
                                       f"job={job_id}"], stdout=subprocess.PIPE,
                                      cwd="/home/alexander/PycharmProjects/Megahackathon_T17/src/parse_news/parse_news")
        proc_result3 = subprocess.run([f"curl",
                                       f"http://localhost:6800/cancel.json",
                                       f"-d",
                                       f"project=parse_news",
                                       f"-d",
                                       f"job={job_id}"], stdout=subprocess.PIPE,
                                      cwd="/home/alexander/PycharmProjects/Megahackathon_T17/src/parse_news/parse_news")
        return "Spider STOPPED"
    except Exception as e:
        print(e)
        return {"status": "error",
                "data": e,
                "details": e}


@get_temp_router.get("/temp/article/count/all", response_model=Count)
# response_model=OfferSearchResult, operation_id="offer_search"
async def whole_quantity(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(func.count(temp_article.c.id))
        result = await session.execute(query)
        return result.scalar()
    except Exception as e:
        print(e)
        return {"status": "error",
                "data": e,
                "details": e}


@get_temp_router.get("/temp/article/single/{item_id}",
                     response_model=List[News])  # response_model=OfferSearchResult, operation_id="offer_search"
async def get_news_by_id(item_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(temp_article).where(temp_article.c.id == item_id)
        result = await session.execute(query)
        return result.all()
    except Exception as e:
        print(e)
        return {"status": "error",
                "data": e,
                "details": e}


@get_temp_router.get("/temp/many/{last_n}", response_model=List[News])
async def get_last_published(last_n: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(temp_article).order_by(temp_article.c.published_at.desc()).limit(last_n)
        result = await session.execute(query)
        return result.all()
    except Exception as e:
        print(e)
        return {"status": "error",
                "data": e,
                "details": e}


@get_temp_router.get("/temp/tags/unique",
                     response_model=List[Tag])  # response_model=OfferSearchResult, operation_id="offer_search"
async def get_unique_tags(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(temp_article.c.tag).distinct()
        result = await session.execute(query)
        return result.all()
    except Exception as e:
        print(e)
        return {"status": "error",
                "data": e,
                "details": e}


@get_temp_router.get("/temp/origins/unique", response_model=List[Origin])
# response_model=OfferSearchResult, operation_id="offer_search"
async def get_unique_origins(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(temp_article.c.parsed_from).distinct()
        result = await session.execute(query)
        return result.all()
    except Exception as e:
        print(e)
        return {"status": "error",
                "data": e,
                "details": e}


@get_temp_router.post("/temp/filter",
                      response_model=List[News])  # response_model=OfferSearchResult, operation_id="offer_search"
async def filter_news(username: UserName, spider: Spider, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(temp_article).filter(temp_article.c.username == username.name,
                                            temp_article.c.spidername == spider.name,
                                            ).order_by(temp_article.c.published_at.desc())
        result = await session.execute(query)
        return result.all()
    except Exception as e:
        print(e)
        return {"status": "error",
                "data": e,
                "details": e}


@get_temp_router.get("/temp/filter_kw/{key_word}", response_model=List[News])
async def filter_news_by_key_word(key_word: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(temp_article).where(temp_article.c.ml_key_words.ilike(f"%{key_word}%")).order_by(
            temp_article.c.published_at.desc())
        result = await session.execute(query)
        return result.all()
    except Exception as e:
        return {"status": "error",
                "data": e,
                "details": e}


@get_temp_router.get("/temp/filter_t/{tag}", response_model=List[News])
async def filter_news_by_tag(tag: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(temp_article).where(temp_article.c.tag.ilike(f"%{tag}%")).order_by(
            temp_article.c.published_at.desc())
        result = await session.execute(query)
        return result.all()
    except Exception as e:
        return {"status": "error",
                "data": e,
                "details": e}

#
# if __name__ == "__main__":
#     get_news_by_id()
