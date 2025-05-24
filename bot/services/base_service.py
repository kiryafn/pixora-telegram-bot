from abc import ABC
from typing import Generic, TypeVar, Sequence
from bot.models import Base
from bot.repositories.base_repository import BaseRepository

M = TypeVar("M", bound=Base)

class BaseService(ABC, Generic[M]):
    def __init__(self, repository: BaseRepository[M]) -> None:
        self.repository = repository

    async def get_by_id(self, obj_id: int) -> M | None:
        return await self.repository.get_by_id(obj_id)

    async def get_all(self) -> Sequence[M]:
        return await self.repository.get_all()

    async def save(self, entity: M) -> None:
        await self.repository.save(entity)

    async def delete_by_id(self, obj_id: int) -> None:
        await self.repository.delete_by_id(obj_id)