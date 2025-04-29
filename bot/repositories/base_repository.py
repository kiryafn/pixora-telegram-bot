from typing import Generic, TypeVar, Type, Sequence
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import async_session

from bot.models import Base

T = TypeVar("T", bound=Base)

class BaseRepository(Generic[T]):
    model: Type[T]

    def __init__(self, model: Type[T]):
        self.model = model

    async def get_by_id(self, obj_id: int) -> T | None:
        async with async_session() as session:
            result = await session.execute(select(self.model).where(obj_id == self.model.id))
            return result.scalar_one_or_none() #returns one obj or none is more

    async def get_all(self) -> Sequence[T]:
        async with async_session() as session:
            result = await session.execute(select(self.model))
            return result.scalars().all()

    async def save(self, obj: T) -> None:
        async with async_session() as session:
            session.add(obj)
            await session.commit()

    async def delete_by_id(self, obj_id: int) -> None:
        async with async_session() as session:
            await session.execute(delete(self.model).where(obj_id == self.model.id))
            await session.commit()

    async def filter_by(self, **kwargs) -> Sequence[T]:
        async with async_session() as session:
            result = await session.execute(select(self.model).filter_by(**kwargs))
            return result.scalars().all()
