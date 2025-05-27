from __future__ import annotations

from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.models import Base


class City(Base):
    __tablename__ = 'cities'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    country_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("countries.id"), nullable=False)

    country: Mapped["Country"] = relationship(
        "Country",
        back_populates="cities",
        lazy="selectin",
    )
    job_preferences: Mapped[list["JobPreference"]] = relationship(
        "JobPreference",
        back_populates="city",
        lazy="selectin",
    )
