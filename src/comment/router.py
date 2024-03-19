from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.comment.models import Comment
from src.comment.schemas import CommentUpdate
from src.database import get_async_session
from src.auth.base_config import current_user

router = APIRouter(
    prefix="/comment",
    tags=["comment"]
)


@router.get("")
async def get_all_user_comments(user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    if user.user_type in ["admin", "manager"]:
        query = select(Comment).where(Comment.author_id == user.id)
    else:
        query = select(Comment).where(Comment.author_id == user.id, Comment.is_moderated == True)
    result = await session.execute(query)
    return result.mappings().all()


@router.patch("")
async def update_comment(new_comm: CommentUpdate,
                         user: User = Depends(current_user),
                         session: AsyncSession = Depends(get_async_session)):
    if user.user_type not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="YOU_CAN_NOT_EDIT_COMMENTS")
    query = select(Comment).where(Comment.id == new_comm.id)
    result = await session.execute(query)
    executor = result.mappings().first()
    if executor is None:
        raise HTTPException(status_code=404, detail="COMMENT_NOT_EXIST")
    stmt = ((update(Comment)
             .where(Comment.id == new_comm.id))
            .values(body=new_comm.body,
                    is_moderated=new_comm.is_moderated))
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.delete("/{comment_id}")
async def delete_comment(comment_id: int,
                         user: User = Depends(current_user),
                         session: AsyncSession = Depends(get_async_session)):
    if user.user_type not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="YOU_CAN_NOT_EDIT_COMMENTS")
    query = select(Comment).where(Comment.id == comment_id)
    result = await session.execute(query)
    executor = result.mappings().first()
    if executor is None:
        raise HTTPException(status_code=404, detail="COMMENT_NOT_EXIST")
    stmt = delete(Comment).where(Comment.id == comment_id)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
