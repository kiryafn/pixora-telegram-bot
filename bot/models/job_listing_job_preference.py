from sqlalchemy import Table, Integer, Column, ForeignKey

from bot.models import Base

job_listing_job_preference = Table(
    'job_listing_job_preference', Base.metadata,
    Column('job_listing_id', Integer, ForeignKey('job_listings.id'), primary_key=True),
    Column('job_preference_id', Integer, ForeignKey('job_preferences.id'), primary_key=True)
)
