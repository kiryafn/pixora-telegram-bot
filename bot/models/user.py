from __future__ import annotations
from datetime import datetime

from sqlalchemy import BigInteger, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from bot.models import Base
from bot.models.user_job_preference import user_job_preference


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(255), nullable=True, default="NO_DATA")
    language: Mapped[str] = mapped_column(String(10), default="en")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    job_preferences: Mapped[list["JobPreference"]] = relationship("JobPreference", secondary=user_job_preference, back_populates="users")
    request_logs: Mapped[list["RequestLog"]] = relationship("RequestLog", back_populates="user", cascade="all, delete-orphan")
