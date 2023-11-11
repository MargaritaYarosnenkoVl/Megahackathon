from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.parse_news.models import article
from src.parse_news.parse_news.spiders import naked_science_spider

router = APIRouter(prefix="/add_naked_science_news",
                   tags=["Add news"])


@router.get("/")
async def add_naked_science(session: AsyncSession = Depends(get_async_session)):
    # stmt = insert(article).values()
    # await session.execute(stmt)
    # await session.commit()
    return


if __name__ == "__main__":
    add_naked_science()
