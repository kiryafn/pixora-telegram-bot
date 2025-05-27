from sqlalchemy import Table, Column, BigInteger, Boolean, ForeignKey
from bot.models import Base

job_listing_job_preference = Table(
    "job_listing_job_preference",
    Base.metadata,
    Column(
        "job_listing_id",
        BigInteger,
        ForeignKey("job_listings.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "job_preference_id",
        BigInteger,
        ForeignKey("job_preferences.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column("is_seen", Boolean, nullable=False, default=False),
)