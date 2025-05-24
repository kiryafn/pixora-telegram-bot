from __future__ import annotations
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, relationship, mapped_column

from bot.models import Base


class RequestLog(Base):
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