from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from tokenizer.tokenize_from_db import main as main_tokenizer
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


fill_ml = APIRouter(prefix="/ml",
                    tags=["Fill key words"])


@fill_ml.get("/fill_key_words")
async def fill_key_words(session: AsyncSession = Depends(get_async_session)):
    try:
        main_tokenizer()
        return
    except Exception as e:
        print(e)
        return {"status": "error",
                "data": e,
                "details": e
                }
    finally:
        pass
