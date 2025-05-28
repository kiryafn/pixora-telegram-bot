from __future__ import annotations

from sqlalchemy import BigInteger, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.models import Base
from bot.models.listing_preference import ListingPreference


class JobPreference(Base):
    """
    Represents a user's job preference configuration.

    Used to define criteria that a user is looking for in job listings,
    such as preferred job title, company, minimum salary, and location.

    Attributes:
        id (int): Unique identifier for the job preference.
        title (str): Desired job title or position.
        company (str | None): Preferred company name (optional).
        min_salary (float): Minimum acceptable salary.
        city_id (int): Foreign key referencing the preferred city.
        user_id (int): Foreign key referencing the user.
        city (City): The city associated with this job preference.
        user (User): The user who owns this job preference.
        listing_preferences (list[ListingPreference]): Join table linking to matching job listings.
        job_listings (list[JobListing]): Job listings matched to this preference via `listing_preferences`.
    """

    __tablename__ = "job_preferences"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    company: Mapped[str] = mapped_column(String(255), nullable=True)
    min_salary: Mapped[float] = mapped_column(Float, nullable=False)
    city_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("cities.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)

    city: Mapped["City"] = relationship(
        "City",
        back_populates="job_preferences",
        lazy="selectin"
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="job_preferences",
        lazy="selectin"
    )

    listing_preferences: Mapped[list[ListingPreference]] = relationship(
        "ListingPreference",
        back_populates="job_preference",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    job_listings: Mapped[list["JobListing"]] = relationship(
        "JobListing",
        secondary="listing_preferences",
        back_populates="job_preferences",
        lazy="selectin",
    )