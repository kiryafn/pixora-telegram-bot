from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from bot.configuration.database import async_session
from bot.models import City
from bot.models import JobPreference
from bot.repositories import BaseRepository


class JobPreferenceRepository(BaseRepository[JobPreference]):
    """
    Repository for managing JobPreference entities.

    Extends BaseRepository with additional methods for retrieving and deleting
    job preferences by user ID. Also supports eager loading of related city and country data.
    """

    def __init__(self) -> None:
        """
        Initializes the repository with the JobPreference model.
        """
        super().__init__(JobPreference)

    async def get_by_user_id(self, user_id: int) -> JobPreference:
        """
        Retrieves the job preference for a specific user by their ID.

        This method also eagerly loads the related city and country information.

        Args:
            user_id (int): The ID of the user whose job preference is being queried.

        Returns:
            JobPreference: The job preference record for the user, or None if not found.
        """
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
        """
        Deletes the job preference associated with a specific user.

        Args:
            user_id (int): The ID of the user whose job preference should be deleted.
        """
        async with async_session() as session:
            stmt = delete(JobPreference).where(JobPreference.user_id == user_id)
            await session.execute(stmt)
            await session.commit()


# Singleton instance for accessing job preferences
job_preference_repository = JobPreferenceRepository()