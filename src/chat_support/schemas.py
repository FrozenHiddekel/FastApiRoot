from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import BigInteger


class CommentRead(BaseModel):
    id: BigInteger
    body: str
    username: str
    tg_user_id: BigInteger
    posted_at: datetime

    class Config:
        from_attributes = True
