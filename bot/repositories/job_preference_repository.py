from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from bot.core.data import async_session
from bot.models import City
from bot.models.job_preference import JobPreference
from bot.repositories import BaseRepository


class JobPreferenceRepository(BaseRepository[JobPreference]):
    def __init__(self) -> None:
        super().__init__(JobPreference)

    async def get_by_user_id(self, user_id: int) -> JobPreference:
        async with async_session() as session:
            stmt = (
                select(JobPreference)
                .where(JobPreference.user_id == user_id)
                .options(
                    selectinload(JobPreference.city)
                    .selectinload(City.country)
                )
            )
            result = await session.execute(stmt)
            return result.scalars().first()

    async def delete_by_user_id(self, user_id: int) -> None:
        async with async_session() as session:
            stmt = delete(JobPreference).where(JobPreference.user_id == user_id)
            await session.execute(stmt)
            await session.commit()


job_preference_repository = JobPreferenceRepository()
