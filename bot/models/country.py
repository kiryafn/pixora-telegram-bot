# bot/models/country.py
from __future__ import annotations

from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from bot.models import Base


class Country(Base):
    __tablename__ = 'countries'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    # связь со списком городов оставляем
    cities: Mapped[list["City"]] = relationship("City", back_populates="country")

    # removed job_preferences relationship — 
    # теперь все job_preferences можно получать через country.cities