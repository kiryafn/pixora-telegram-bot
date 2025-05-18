from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column
from bot.models.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(255), nullable=True, default="NO_DATA")
    language: Mapped[str] = mapped_column(String(10), default="en")
