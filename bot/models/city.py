from __future__ import annotations

from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.models import Base


class City(Base):
    """
    Represents a city entity in the database.

    Attributes:
        id (int): Unique identifier for the city.
        name (str): Name of the city.
        country_id (int): Foreign key referencing the associated country.
        country (Country): The country this city belongs to.
        job_preferences (list[JobPreference]): Job preferences associated with this city.
    """

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