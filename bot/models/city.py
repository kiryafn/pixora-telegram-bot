from __future__ import annotations

from sqlalchemy import String, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, relationship, mapped_column

from bot.models import Base


class City(Base):
    __tablename__ = 'cities'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    country_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("countries.id"), nullable=False)

    country: Mapped["Country"] = relationship("Country", back_populates="cities")
    job_preferences: Mapped[list["JobPreference"]] = relationship("JobPreference", back_populates="city")
    job_listings: Mapped[list["JobListing"]] = relationship("JobListing", back_populates="city")

