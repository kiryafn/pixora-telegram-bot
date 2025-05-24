from __future__ import annotations
from datetime import datetime

from sqlalchemy import BigInteger, String, Float, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.models import Base
from bot.models.job_listing_job_preference import job_listing_job_preference


class JobListing(Base):
    __tablename__ = 'job_listings'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    job_title: Mapped[str] = mapped_column(String(255), nullable=False)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    salary: Mapped[float] = mapped_column(Float, nullable=False)
    job_url: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    date_posted: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_seen: Mapped[bool] = mapped_column(Boolean, default=False)
    seen_marker: Mapped[str] = mapped_column(String(100), nullable=True)

    job_preferences: Mapped[list["JobPreference"]] = relationship(
        "JobPreference",
        secondary=job_listing_job_preference,
        back_populates="job_listings",
    )
