from __future__ import annotations

from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.models import Base


class Country(Base):
    """
    Represents a country entity in the database.

    Attributes:
        id (int): Unique identifier for the country.
        name (str): Name of the country.
        cities (list[City]): List of cities that belong to this country.
    """

    __tablename__ = 'countries'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    cities: Mapped[list["City"]] = relationship(
        "City",
        back_populates="country",
        lazy="selectin",
    )