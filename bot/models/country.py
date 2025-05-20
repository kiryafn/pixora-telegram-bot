from __future__ import annotations

from sqlalchemy import String, BigInteger
from sqlalchemy.orm import Mapped, relationship, mapped_column

from bot.models import Base


class Country(Base):
    __tablename__ = 'countries'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    cities: Mapped[list["City"]] = relationship("City", back_populates="country")
    job_preferences: Mapped[list["JobPreference"]] = relationship("JobPreference", back_populates="country")