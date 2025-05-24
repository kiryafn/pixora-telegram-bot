from __future__ import annotations
from datetime import datetime

from sqlalchemy import BigInteger, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from bot.models import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(255), nullable=True)
    language: Mapped[str] = mapped_column(String(10), default="en")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    job_preferences: Mapped[list["JobPreference"]] = relationship(
        "JobPreference",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    request_logs: Mapped[list["RequestLog"]] = relationship(
        "RequestLog",
        back_populates="user",
        cascade="all, delete-orphan"
    )
