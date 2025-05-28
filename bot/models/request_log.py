from __future__ import annotations
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, relationship, mapped_column

from bot.models import Base


class RequestLog(Base):
    """
    Represents a log entry for a user's request to the system.

    This model stores timing information about how long a specific user's request took to process.
    Useful for performance monitoring and auditing.

    Attributes:
        id (int): Unique identifier for the request log entry.
        request_time (datetime): Timestamp when the request was made. Defaults to the current time.
        response_time (float): Duration of the response time in seconds.
        user_id (int): Foreign key referencing the user who made the request.
        user (User): The user associated with the request.
    """

    __tablename__ = "request_logs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    request_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    response_time: Mapped[float] = mapped_column(Float)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship(
        "User",
        back_populates="request_logs",
        foreign_keys=[user_id]
    )