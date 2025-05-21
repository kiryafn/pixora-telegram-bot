from typing import Generic, TypeVar, Type, Sequence
from sqlalchemy import select, delete
from bot.core.data import async_session
from bot.models import Base

M = TypeVar("M", bound=Base)

class BaseRepository(Generic[M]):
    def __init__(self, model: Type[M]) -> None:
        self.model = model

    async def get_by_id(self, obj_id: int) -> M | None:
        async with async_session() as session:
            stmt = select(self.model).where(obj_id == self.model.id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def get_all(self) -> Sequence[M]:
        async with async_session() as session:
            stmt = select(self.model)
            result = await session.execute(stmt)
            return result.scalars().all()

    async def save(self, obj: M) -> None:
        async with async_session() as session:
            session.add(obj)
            await session.commit()

    async def delete_by_id(self, obj_id: int) -> None:
        async with async_session() as session:
            stmt = delete(self.model).where(obj_id == self.model.id)
            await session.execute(stmt)
            await session.commit()

    async def filter_by(self, **kwargs) -> Sequence[M]:
        async with async_session() as session:
            stmt = select(self.model).filter_by(**kwargs)
            result = await session.execute(stmt)
            return result.scalars().all()