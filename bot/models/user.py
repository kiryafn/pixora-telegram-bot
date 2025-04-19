from sqlalchemy import Column, BigInteger, String, DateTime, func
from bot.core.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    username = Column(String, nullable=True)
    language_code = Column(String, default="en", name="language")