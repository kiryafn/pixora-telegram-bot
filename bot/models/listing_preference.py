from __future__ import annotations
from sqlalchemy import BigInteger, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.models import Base


class ListingPreference(Base):
    """
    Association table linking job listings to job preferences.

    This table represents a many-to-many relationship between job listings and job preferences.
    Each row tracks whether a specific job listing has been matched to a given user preference
    and whether the user has seen the job listing.

    Attributes:
        id (int): Unique identifier for the listing-preference link.
        job_listing_id (int): Foreign key referencing the related job listing.
        job_preference_id (int): Foreign key referencing the related job preference.
        is_seen (bool): Indicates whether the listing has already been shown to the user.
        job_listing (JobListing): The associated job listing.
        job_preference (JobPreference): The associated job preference.

    Constraints:
        Unique constraint on (job_listing_id, job_preference_id) to avoid duplicates.
    """

    __tablename__ = "listing_preferences"
    __table_args__ = (
        UniqueConstraint(
            "job_listing_id",
            "job_preference_id",
            name="uq_listing_preference__job_listing__job_pref",
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    job_listing_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("job_listings.id", ondelete="CASCADE"),
        nullable=False,
    )
    job_preference_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("job_preferences.id", ondelete="CASCADE"),
        nullable=False,
    )
    is_seen: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    job_listing: Mapped["JobListing"] = relationship(
        "JobListing",
        back_populates="listing_preferences",
    )
    job_preference: Mapped["JobPreference"] = relationship(
        "JobPreference",
        back_populates="listing_preferences",
    )