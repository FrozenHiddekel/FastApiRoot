from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.comment.models import Comment
from src.database import get_async_session
from src.auth.base_config import current_user

router = APIRouter(
    prefix="/comment",
    tags=["comment"]
)


@router.get("")
async def get_all_user_comments(user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    query = select(Comment).where(Comment.author_id == user.id)
    result = await session.execute(query)
    return result.mappings().all()
