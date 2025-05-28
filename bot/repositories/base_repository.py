from typing import Generic, TypeVar, Type, Sequence
from sqlalchemy import select, delete
from bot.configuration.database import async_session
from bot.models import Base

M = TypeVar("M", bound=Base)


class BaseRepository(Generic[M]):
    """
    Generic base repository for performing common CRUD operations on SQLAlchemy models.

    This class provides reusable asynchronous methods to retrieve, save, delete, and filter
    model instances using SQLAlchemy ORM and an async session.

    Attributes:
        model (Type[M]): The SQLAlchemy model class associated with this repository.
    """

    def __init__(self, model: Type[M]) -> None:
        """
        Initializes the repository with a specific model class.

        Args:
            model (Type[M]): The model class to operate on.
        """
        self.model = model

    async def get_by_id(self, obj_id: int) -> M | None:
        """
        Retrieves a single object by its primary key.

        Args:
            obj_id (int): The ID of the object to retrieve.

        Returns:
            M | None: The object if found, otherwise None.
        """
        async with async_session() as session:
            stmt = select(self.model).where(obj_id == self.model.id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def get_all(self) -> Sequence[M]:
        """
        Retrieves all instances of the model.

        Returns:
            Sequence[M]: A list of all model instances.
        """
        async with async_session() as session:
            stmt = select(self.model)
            result = await session.execute(stmt)
            return result.scalars().all()

    async def save(self, obj: M) -> M:
        """
        Saves (inserts or updates) the given object in the database.

        Args:
            obj (M): The model instance to save.

        Returns:
            M: The saved (and refreshed) model instance.
        """
        async with async_session() as session:
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            return obj

    async def delete_by_id(self, obj_id: int) -> None:
        """
        Deletes an object from the database by its primary key.

        Args:
            obj_id (int): The ID of the object to delete.
        """
        async with async_session() as session:
            stmt = delete(self.model).where(obj_id == self.model.id)
            await session.execute(stmt)
            await session.commit()

    async def filter_by(self, **kwargs) -> Sequence[M]:
        """
        Filters records by column values.

        Args:
            **kwargs: Column filters as keyword arguments (e.g., name='John').

        Returns:
            Sequence[M]: A list of objects matching the filter criteria.
        """
        async with async_session() as session:
            stmt = select(self.model).filter_by(**kwargs)
            result = await session.execute(stmt)
            return result.scalars().all()