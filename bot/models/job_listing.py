from __future__ import annotations

from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.models import Base
from bot.models.job_listing_job_preference import job_listing_job_preference


class JobListing(Base):
    __tablename__ = 'job_listings'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    job_title: Mapped[str] = mapped_column(String(255), nullable=False)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    company_logo_url: Mapped[str] = mapped_column(String(1000), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    salary: Mapped[str] = mapped_column(String(255), nullable=False)
    #date_posted: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    #TODO: deadline date
    job_schedule: Mapped[str] = mapped_column(String(255), nullable=False)


    job_url: Mapped[str] = mapped_column(String(1000), nullable=False, unique=True)
    # is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    job_preferences: Mapped[list["JobPreference"]] = relationship(
        "JobPreference",
        secondary=job_listing_job_preference,
        back_populates="job_listings",
        lazy="selectin",
    )
