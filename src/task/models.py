from datetime import datetime
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, BigInteger
from src.auth.models import User
from src.database import Base


class Task(Base):
    __tablename__ = "task"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(128), nullable=False)
    description = Column(String(4096), nullable=True)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=True)
    author_id = Column(BigInteger, ForeignKey(User.id, ondelete="CASCADE"), nullable=False)
    executor_id = Column(BigInteger, ForeignKey(User.id, ondelete="SET NULL"), nullable=True)
    priority = Column(Integer, nullable=True)
