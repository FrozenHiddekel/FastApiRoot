from datetime import datetime
from sqlalchemy import Column,  String, ForeignKey, TIMESTAMP, BigInteger

from src.auth.models import User
from src.database import Base
from src.task.models import Task


class Comment(Base):
    __tablename__ = "comment"
    id = Column(BigInteger, primary_key=True, autoincrement=True, unique=True)
    body = Column(String(4096), nullable=False)
    author_id = Column(BigInteger, ForeignKey(User.id, ondelete="CASCADE"), nullable=False)
    task_id = Column(BigInteger, ForeignKey(Task.id, ondelete="CASCADE"), nullable=False)
    posted_at = Column(TIMESTAMP, default=datetime.utcnow)


