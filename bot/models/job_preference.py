from __future__ import annotations

from sqlalchemy import BigInteger, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from bot.models import Base
from bot.models.job_listing_job_preference import job_listing_job_preference


class JobPreference(Base):
    __tablename__ = "job_preferences"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    company: Mapped[str] = mapped_column(String(255), nullable=True)
    min_salary: Mapped[float] = mapped_column(Float, nullable=False)
    city_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("cities.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)

    city: Mapped["City"] = relationship(
        "City",
        back_populates="job_preferences"
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="job_preferences"
    )
    job_listings: Mapped[list["JobListing"]] = relationship(
        "JobListing",
        secondary=job_listing_job_preference,
        back_populates="job_preferences"
    )
