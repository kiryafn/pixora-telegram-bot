from __future__ import annotations
from datetime import datetime

from sqlalchemy import BigInteger, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.models import Base
from bot.models.listing_preference import ListingPreference


class JobListing(Base):
    __tablename__ = "job_listings"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    job_title: Mapped[str] = mapped_column(String(255), nullable=False)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    company_logo_url: Mapped[str] = mapped_column(String(1000), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    salary: Mapped[str] = mapped_column(String(255), nullable=False)
    job_schedule: Mapped[str] = mapped_column(String(255), nullable=False)
    job_url: Mapped[str] = mapped_column(String(1000), nullable=False, unique=True)
    #is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    listing_preferences: Mapped[list[ListingPreference]] = relationship(
        "ListingPreference",
        back_populates="job_listing",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    job_preferences: Mapped[list["JobPreference"]] = relationship(
        "JobPreference",
        secondary="listing_preferences",
        back_populates="job_listings",
        lazy="selectin",
    )