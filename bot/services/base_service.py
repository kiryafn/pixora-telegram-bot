from abc import ABC
from typing import Generic, TypeVar, Sequence

from bot.models import Base
from bot.repositories import BaseRepository

M = TypeVar("M", bound=Base)


class BaseService(ABC, Generic[M]):
    """
    Abstract base service providing generic CRUD operations for any SQLAlchemy model.

    Designed to be extended by concrete services (e.g., UserService, JobService),
    this class delegates all operations to the corresponding repository layer.

    Attributes:
        repository (BaseRepository[M]): The repository instance responsible for database operations.
    """

    def __init__(self, repository: BaseRepository[M]) -> None:
        """
        Initializes the base service with the given repository.

        Args:
            repository (BaseRepository[M]): A repository instance to perform database operations.
        """
        self.repository = repository

    async def get_by_id(self, obj_id: int) -> M | None:
        """
        Retrieves a single entity by its primary key.

        Args:
            obj_id (int): The ID of the entity to retrieve.

        Returns:
            M | None: The entity if found, otherwise None.
        """
        return await self.repository.get_by_id(obj_id)

    async def get_all(self) -> Sequence[M]:
        """
        Retrieves all entities of the model.

        Returns:
            Sequence[M]: A list of all entities.
        """
        return await self.repository.get_all()

    async def save(self, entity: M) -> M:
        """
        Persists an entity to the database (insert or update).

        Args:
            entity (M): The entity instance to save.

        Returns:
            M: The saved and refreshed entity.
        """
        return await self.repository.save(entity)

    async def delete_by_id(self, obj_id: int) -> None:
        """
        Deletes an entity by its primary key.

        Args:
            obj_id (int): The ID of the entity to delete.
        """
        await self.repository.delete_by_id(obj_id)