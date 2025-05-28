from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.

    This class serves as the declarative base for SQLAlchemy ORM models.
    All ORM models in the application should inherit from this class
    to automatically include metadata and table bindings.

    Inherits:
        sqlalchemy.orm.DeclarativeBase: SQLAlchemy base class.
    """
    pass