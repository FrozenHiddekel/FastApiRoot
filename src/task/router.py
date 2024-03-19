from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.auth.models import User
from src.comment.models import Comment
from src.comment.schemas import CommentCreate
from src.database import get_async_session
from src.task.models import Task
from src.task.schemas import TaskCreate, TaskUpdate
from src.auth.base_config import fastapi_users


router = APIRouter(
    prefix="/task",
    tags=["task"]
)
current_user = fastapi_users.current_user()


@router.get("")
async def get_all_user_tasks(user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    query = select(Task).where(Task.author_id == user.id)
    result = await session.execute(query)
    return result.mappings().all()


@router.get("/{task_id}")
async def get_task_with_comments(task_id: int,
                                 session: AsyncSession = Depends(get_async_session),
                                 user: User = Depends(current_user)):
    query = select(Task).where(Task.id == task_id)

    if user.user_type in ["admin", "manager"]:
        query2 = select(Comment).where(Comment.task_id == task_id)
    else:
        query2 = select(Comment).where(Comment.task_id == task_id, Comment.is_moderated == True)
    result = await session.execute(query)
    result2 = await session.execute(query2)
    return result.mappings().all() + result2.mappings().all()


@router.post("")
async def create_task(new_task: TaskCreate,
                      user: User = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)):
    query = select(User).where(User.email == new_task.executor_email)
    result = await session.execute(query)
    executor = result.mappings().first()
    if executor is None:
        raise HTTPException(status_code=400, detail="USER_EMAIL_NOT_FOUND")
    id_executor = executor.get("User").id
    stmt = insert(Task).values(title=new_task.title,
                               description=new_task.description,
                               author_id=user.id,
                               executor_id=id_executor,
                               updated_at=datetime.utcnow(),
                               priority=new_task.priority)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.patch("")
async def update_task(new_task: TaskUpdate,
                      user: User = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)):
    author_id = user.id
    query = (select(Task)
             .where(Task.id == new_task.id)
             .where(Task.author_id == author_id))
    result = await session.execute(query)
    executor = result.mappings().first()
    if executor is None:
        raise HTTPException(status_code=403, detail="YOU_DO_NOT_OWN_THIS_TASK")
    query = select(User).where(User.email == new_task.executor_email)
    result = await session.execute(query)
    executor = result.mappings().first()
    if executor is None:
        raise HTTPException(status_code=400, detail="USER_EMAIL_NOT_FOUND")
    id_executor = executor.get("User").id
    stmt = ((update(Task)
            .where(Task.id == new_task.id))
            .values(title=new_task.title,
                    description=new_task.description,
                    author_id=user.id,
                    executor_id=id_executor,
                    updated_at=datetime.utcnow(),
                    priority=new_task.priority))

    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.delete("/{task_id}")
async def delete_task(task_id: int,
                      user: User = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)):
    author_id = user.id
    query = select(Task).where(Task.id == task_id, Task.author_id == author_id)
    result = await session.execute(query)
    executor = result.mappings().first()
    if executor is None:
        raise HTTPException(status_code=403, detail="YOU_DO_NOT_OWN_THIS_TASK")
    stmt = delete(Task).where(Task.id == task_id, Task.author_id == author_id)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}

@router.post("/{task_id}/newcomm")
async def add_comment(comment: CommentCreate,
                      task_id: int,
                      user: User = Depends(current_user),
                      session: Session = Depends(get_async_session)):
    query = select(Task).where(Task.id == task_id)
    result = await session.execute(query)
    executor = result.mappings().first()
    already_moderated = user.user_type in ["admin", "manager"]
    print(executor)
    if executor is None:
        raise HTTPException(status_code=404, detail="TASK_NOT_FOUND")
    stmt = insert(Comment).values(body=comment.body,
                               author_id=user.id,
                               task_id=task_id,
                               is_moderated=already_moderated)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
