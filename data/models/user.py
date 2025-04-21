from datetime import datetime
from sqlalchemy import String, BigInteger, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from bot.core.db import Base


class User(Base):
    __tablename__ = "users"

    #Telegram ID
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    #@username
    username: Mapped[str] = mapped_column(String, nullable=True)

    #Name and surname
    full_name: Mapped[str] = mapped_column(String, nullable=True)

    #Telegram interface language
    language_code: Mapped[str] = mapped_column(String, default="en")

    #User turned off bot or no
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    #When I registered
    registered_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    #The last time was updated
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())