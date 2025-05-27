from __future__ import annotations
from sqlalchemy import BigInteger, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.models import Base

class ListingPreference(Base):
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