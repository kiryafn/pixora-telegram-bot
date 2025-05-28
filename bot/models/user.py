from __future__ import annotations
from datetime import datetime

from sqlalchemy import BigInteger, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from bot.models import Base


class User(Base):
    """
    Represents an application user.

    Stores information about the user's identity, preferences, status, and activity timestamps.
    Connected to job preferences and request logs via one-to-many relationships.

    Attributes:
        id (int): Unique identifier for the user.
        username (str | None): Telegram or application username (optional).
        language (str): Language preference of the user (e.g., 'en', 'pl'). Defaults to 'en'.
        is_active (bool): Indicates if the user account is active. Defaults to True.
        is_banned (bool): Indicates if the user is banned. Defaults to False.
        created_at (datetime): Timestamp of account creation.
        updated_at (datetime): Timestamp of the last update to the user's record.

        job_preferences (list[JobPreference]): List of job search preferences defined by the user.
        request_logs (list[RequestLog]): Log entries of the user's API or interface interactions.
    """

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