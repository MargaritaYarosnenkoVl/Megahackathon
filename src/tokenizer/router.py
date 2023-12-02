from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from tokenizer.tokenize_from_db import main as main_tokenizer
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import logging

logger = logging.getLogger("app")

fill_ml = APIRouter(prefix="/ml",
                    tags=["Fill key words"])


@fill_ml.get("/fill_key_words")
async def fill_key_words(table_name: str, session: AsyncSession = Depends(get_async_session)):
    try:
        main_tokenizer(table_name)
        return "Key words added"
    except Exception as e:
        print(e)
        logger.info(e)
        return {"status": "error",
                "data": e,
                "details": e
                }
    finally:
        pass
