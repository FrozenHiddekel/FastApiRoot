from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.chat_support.models import ChatSupport
from src.database import get_async_session

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)


@router.get("")
async def get_all_comments(limit: int = 1, offset: int = 0, session: AsyncSession = Depends(get_async_session)):
    query = select(ChatSupport).offset(offset).limit(limit)
    result = await session.execute(query)
    return result.mappings().all()
