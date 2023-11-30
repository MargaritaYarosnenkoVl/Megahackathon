import logging
import subprocess
import json
from typing import List, Any
from fastapi import APIRouter, Depends
from sqlalchemy import insert, select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from .models import article, temp_article
from .schemas import (MainNews,
                      TempNews,
                      NewsID,
                      NewsFilter,
                      Tag,
                      Origin,
                      SpiderName,
                      Count,
                      JobID,
                      UserName,
                      UserNameBase,
                      Spider,
                      SpiderOrigin,
                      ParsedFrom, DeleteNews)

get_base_router = APIRouter(prefix="/get",
                            tags=["Get News"])

get_temp_router = APIRouter(prefix="/get",
                            tags=["Get Temp News"])

schedule_parser_router = APIRouter(prefix="/schedule",
                                   tags=["Schedule parser/spider"])

logger = logging.getLogger('app')


# --- ARTICLE --- #
@get_base_router.get("/count/all",
                     response_model=Count)
async def whole_quantity(session: AsyncSession = Depends(get_async_session)):
    try:
        logger.info(f"Try to count all news in table article")
        query = select(func.count(article.c.id)).where(article.c.title.is_not(None))
        result = await session.execute(query)
        logger.info(f"Count all news in table article")
        return result.scalar()
    except Exception as e:
        print(e)
        return {"status": "error",
                "data": e,
                "details": e}


@get_base_router.get("/single/{item_id}", response_model=List[MainNews])
async def get_news_by_id(item_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        logger.info(f"Try to get news with id={item_id} from article table")
        query = select(article).where(article.c.id == item_id)
        result = await session.execute(query)
        logger.info(f"Got news with id={item_id} from article table")
        return result.all()
    except Exception as e:
        print(e)
        logger.debug(e)
        return {"status": "error",
                "data": e,
                "details": e}


@get_base_router.get("/many/{last_n}", response_model=List[MainNews])
async def get_last_published(last_n: int, session: AsyncSession = Depends(get_async_session)):
    try:
        logger.info(f"Try to get news N = {last_n} from article table")
        query = select(article).order_by(article.c.published_at.desc()).limit(last_n)
        result = await session.execute(query)
        logger.info(f"Got {last_n} from article table")
        return result.all()
    except Exception as e:
        print(e)
        logger.debug(e)
        return {"status": "error",
                "data": e,
                "details": e}


@get_base_router.get("/tags/unique", response_model=List[Tag])
async def get_unique_tags(session: AsyncSession = Depends(get_async_session)):
    try:
        logger.info(f"Try to get unique tags from article table")
        query = select(article.c.tag).distinct()
        result = await session.execute(query)
        logger.info(f"Got unique tags from article table")
        return result.all()
    except Exception as e:
        print(e)
        logger.debug(e)
        return {"status": "error",
                "data": e,
                "details": e}


@get_base_router.get("/origins/unique", response_model=List[Origin])
async def get_unique_origins(session: AsyncSession = Depends(get_async_session)):
    try:
        logger.info(f"Try to get unique origins from article table")
        query = select(article.c.parsed_from).distinct()
        result = await session.execute(query)
        logger.info(f"Got unique origins from article table")
        return result.all()
    except Exception as e:
        print(e)
        logger.debug(e)
        return {"status": "error",
                "data": e,
                "details": e}


@get_base_router.post("/filter", response_model=List[MainNews])
async def filter_news(data: NewsFilter, session: AsyncSession = Depends(get_async_session)):
    try:
        logger.info(f"Try to filter by {data.parsed_from}, "
                    f"from {data.published_at_low},"
                    f"to {data.published_at_high} from article table")
        query = select(article).filter(article.c.parsed_from == data.parsed_from,
                                       article.c.published_at >= data.published_at_low,
                                       article.c.published_at <= data.published_at_high
                                       ).order_by(article.c.published_at.desc())
        logger.info("Got filter result")
        result = await session.execute(query)
        return result.all()
    except Exception as e:
        print(e)
        logger.debug(e)
        return {"status": "error",
                "data": e,
                "details": e}


@get_base_router.get("/filter_kw/{key_word}", response_model=List[MainNews])
async def filter_news_by_key_word(key_word: str, session: AsyncSession = Depends(get_async_session)):
    try:
        logger.info(f"Try to filter by {key_word} from article table")
        query = select(article).where(article.c.ml_key_words.ilike(f"%{key_word}%")).order_by(
            article.c.published_at.desc())
        result = await session.execute(query)
        logger.info(f"Got filter result by {key_word} from article table")
        return result.all()
    except Exception as e:
        logger.debug(e)
        return {"status": "error",
                "data": e,
                "details": e}


@get_base_router.get("/filter_t/{tag}", response_model=List[MainNews])
async def filter_news_by_tag(tag: str, session: AsyncSession = Depends(get_async_session)):
    try:
        logger.info(f"Try to filter by {tag} from article table")
        query = select(article).where(article.c.tag.ilike(f"%{tag}%")).order_by(article.c.published_at.desc())
        result = await session.execute(query)
        logger.info(f"Got filter result by {tag} from article table")
        return result.all()
    except Exception as e:
        logger.debug(e)
        return {"status": "error",
                "data": e,
                "details": e}


# --- PARSERS-SPIDERS --- #
@schedule_parser_router.post("/spider", response_model=JobID)
async def launch_spider(origin: SpiderOrigin, username: UserName):
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
        logger.info(f"Try to launch spider {spidername} by {username.name}")
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
        params = json.loads(proc_result.stdout)
        job_id = params["jobid"]
        logger.info(f"Spider {spidername} is launched with params = {params}")
        print("OK", "Please, wait while parser is working. JobID: ", job_id)
        return job_id
    except Exception as e:
        print(e)
        logger.debug(e)
        return {"status": "error",
                "data": e,
                "details": e}


@schedule_parser_router.post("/spider/stop", response_model=JobID)
async def stop_spider(job_id: str):
    try:
        logger.info(f"Try to stop spider with JObID={job_id}")
        for _ in range(3):
            proc_result = subprocess.run([f"curl",
                                          f"http://localhost:6800/cancel.json",
                                          f"-d",
                                          f"project=parse_news",
                                          f"-d",
                                          f"job={job_id}"], stdout=subprocess.PIPE,
                                         cwd="/home/alexander/PycharmProjects/Megahackathon_T17/"
                                             "src/parse_news/parse_news")

        logger.info(f"Spider with JobID={job_id} is STOPPED")
        return "Spider STOPPED"
    except Exception as e:
        print(e)
        logger.debug(e)
        return {"status": "error",
                "data": e,
                "details": e}


# --- TEMP_ARTICLE --- #
@get_temp_router.get("/temp/count/all", response_model=Count)
# response_model=OfferSearchResult, operation_id="offer_search"
async def whole_quantity(session: AsyncSession = Depends(get_async_session)):
    try:
        logger.info(f"Try to count all news in table temp_article")
        query = select(func.count(temp_article.c.id))
        result = await session.execute(query)
        logger.info(f"Count all news in table temp_article")
        return result.scalar()
    except Exception as e:
        print(e)
        logger.debug(e)
        return {"status": "error",
                "data": e,
                "details": e}


@get_temp_router.get("/temp/single/{item_id}", response_model=List[MainNews])
async def get_news_by_id(item_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        logger.info(f"Try to get news with id={item_id} from temp_article table")
        query = select(temp_article).where(temp_article.c.id == item_id)
        result = await session.execute(query)
        logger.info(f"Got news with id={item_id} from temp_article table")
        return result.all()
    except Exception as e:
        logger.debug(e)
        return {"status": "error",
                "data": e,
                "details": e}


@get_temp_router.post("/temp/copy_to_main/{item_id}", response_model=Any)
async def copy_news_by_id(item_id: int, username: UserName, session: AsyncSession = Depends(get_async_session)):
    try:
        logger.info("Check for title with username in main")
        # query on title from temp
        query_title = select(temp_article.c.title).where(temp_article.c.id == item_id,
                                                         temp_article.c.username == username.name)
        # get title from temp
        title = await session.execute(query_title)
        query_title_res: str = title.fetchone()[0]
        logger.info(query_title)
        # check title with username in main
        query_on_exist_in_main = select(article).where(article.c.title == query_title_res,
                                                       article.c.username == username.name)
        news_exist_in_main = await session.execute(query_on_exist_in_main)
        is_exist = news_exist_in_main.fetchone()
        if not is_exist:
            logger.info(f"Try to copy news with id={item_id} from temp_article to article table")
            fields_to_copy = ["title", "brief_text", "full_text", "tag", "search_words", "ml_key_words", "parsed_from",
                              "full_text_link", "published_at", "parsed_at", "rating", "counter", "fun_metric",
                              "unique_metric",
                              "simple_metric", "username"]
            query = select(temp_article.c.title, temp_article.c.brief_text, temp_article.c.full_text,
                           temp_article.c.tag, temp_article.c.search_words, temp_article.c.ml_key_words,
                           temp_article.c.parsed_from, temp_article.c.full_text_link, temp_article.c.published_at,
                           temp_article.c.parsed_at, temp_article.c.rating, temp_article.c.counter,
                           temp_article.c.fun_metric, temp_article.c.unique_metric, temp_article.c.simple_metric,
                           temp_article.c.username
                           ).where(temp_article.c.id == item_id,
                                   temp_article.c.username == username.name)
            stmt = article.insert().from_select(fields_to_copy, query)
            await session.execute(stmt)
            await session.commit()
            logger.info(f"News with id={item_id} by {username.name} copied from temp_article to article")
            return "Article was copied"
        else:
            return "Article already exists"
    except TypeError as e:
        logger.debug(e)
        return "Article doesnt exit in temp"
    except Exception as e:
        logger.debug(e)
        return {"status": "error",
                "data": e,
                "details": e}


# @get_temp_router.patch("/temp/single/", response_model=List[TempNews])
# async def patch_news(news: TempNews, session: AsyncSession = Depends(get_async_session)):
#     try:
#         logger.info(f"Try to patch news by id={id} from temp_article table")
#         delete_stmt = delete(temp_article).where(temp_article.c.id == id).returning(id)
#         result = await session.execute(delete_stmt)
#         await session.commit()
#         logger.info(f"News with id={id} is deleted from temp_article table")
#         return result.scalar()
#     except Exception as e:
#         logger.debug(e)
#         return {"status": "error",
#                 "data": e,
#                 "details": e}


@get_temp_router.delete("/temp/single/{id}", response_model=List[DeleteNews] | Any)
async def delete_news_by_id(id: int, username: UserName, session: AsyncSession = Depends(get_async_session)):
    try:
        logger.info(f"Try to delete news by id={id} for {username.name} from temp_article table")
        delete_stmt = delete(temp_article).where(temp_article.c.id == id,
                                                 temp_article.c.username == username.name).returning(id)
        result = await session.execute(delete_stmt)
        await session.commit()
        logger.info(f"News with id={id} is deleted for {username.name} from temp_article table")
        return result.scalar()
    except Exception as e:
        logger.debug(e)
        return {"status": "error",
                "data": e,
                "details": e}


@get_temp_router.delete("/temp/many/all", response_model=List[DeleteNews] | Any)
async def delete_all_news(username: UserName, session: AsyncSession = Depends(get_async_session)):
    try:
        logger.info(f"Try to delete all news for {username} from temp_article table")
        delete_stmt = delete(temp_article).where(temp_article.c.username == username.name)
        result = await session.execute(delete_stmt)
        logger.info(result)
        await session.commit()
        logger.info(f"All News for user {username.name} are deleted from temp_article table")
        return "Articles deleted"
    except Exception as e:
        logger.debug(e)
        return {"status": "error",
                "data": e,
                "details": e}


@get_temp_router.get("/temp/many/{last_n}", response_model=List[MainNews])
async def get_last_published(last_n: int, session: AsyncSession = Depends(get_async_session)):
    try:
        logger.info(f"Try to get news N = {last_n} from temp_article table")
        query = select(temp_article).order_by(temp_article.c.published_at.desc()).limit(last_n)
        result = await session.execute(query)
        logger.info(f"Got {last_n} news from temp_article table")
        return result.all()
    except Exception as e:
        print(e)
        logger.debug(e)
        return {"status": "error",
                "data": e,
                "details": e}


@get_temp_router.get("/temp/tags/unique", response_model=List[Tag])
async def get_unique_tags(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(temp_article.c.tag).distinct()
        result = await session.execute(query)
        return result.all()
    except Exception as e:
        print(e)
        logger.debug(e)
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
        logger.debug(e)
        return {"status": "error",
                "data": e,
                "details": e}


@get_temp_router.post("/temp/filter", response_model=List[MainNews])
async def filter_news(username: UserName, origin: SpiderOrigin, session: AsyncSession = Depends(get_async_session)):
    try:
        logger.info(f"Try to filter by {username.name}, {origin} from temp_article")
        spidername: str = origin.__dict__.get("parsed_from").__dict__.get("_name_")
        logger.debug(f"Got {spidername} name")
        query = select(temp_article).filter(temp_article.c.username == username.name,
                                            temp_article.c.spidername == spidername,
                                            ).order_by(temp_article.c.published_at.desc())
        logger.info("Got filter result")
        result = await session.execute(query)
        return result.all()
    except Exception as e:
        print(e)
        logger.debug(e)
        return {"status": "error",
                "data": e,
                "details": e}


@get_temp_router.get("/temp/filter_kw/{key_word}", response_model=List[MainNews])
async def filter_news_by_key_word(key_word: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(temp_article).where(temp_article.c.ml_key_words.ilike(f"%{key_word}%")).order_by(
            temp_article.c.published_at.desc())
        result = await session.execute(query)
        return result.all()
    except Exception as e:
        logger.debug(e)
        return {"status": "error",
                "data": e,
                "details": e}


@get_temp_router.get("/temp/filter_t/{tag}", response_model=List[MainNews])
async def filter_news_by_tag(tag: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(temp_article).where(temp_article.c.tag.ilike(f"%{tag}%")).order_by(
            temp_article.c.published_at.desc())
        result = await session.execute(query)
        return result.all()
    except Exception as e:
        logger.debug(e)
        return {"status": "error",
                "data": e,
                "details": e}

#
# if __name__ == "__main__":
#     get_news_by_id()
