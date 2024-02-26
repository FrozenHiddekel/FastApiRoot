from datetime import datetime
from sqlalchemy import Column, String, TIMESTAMP, BigInteger
from src.database import Base


class ChatSupport(Base):
    __tablename__ = "chat_support"
    id = Column(BigInteger, primary_key=True)
    body = Column(String(length=2048), nullable=False)
    username = Column(String(length=512), nullable=False)
    tg_user_id = Column(BigInteger, nullable=False)
    posted_at = Column(TIMESTAMP, default=datetime.utcnow)
