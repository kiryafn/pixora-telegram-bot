from sqlalchemy import Table, Integer, Column, ForeignKey

from bot.models import Base

user_job_preference = Table(
    'user_job_preferences', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('preference_id', Integer, ForeignKey('job_preferences.id'), primary_key=True)
)