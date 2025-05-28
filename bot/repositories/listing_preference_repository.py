from typing import Sequence

from sqlalchemy import select

from bot.configuration.database import async_session
from bot.models import ListingPreference, JobListing
from bot.repositories import BaseRepository


class ListingPreferenceRepository(BaseRepository[ListingPreference]):
    """
    Repository for managing ListingPreference entities.

    Provides custom queries for accessing listing-preference mappings based on
    job preference or job listing IDs, including support for filtering unseen listings.
    """

    def __init__(self) -> None:
        """
        Initializes the repository with the ListingPreference model.
        """
        super().__init__(ListingPreference)

    async def get_all_by_preference_id(self, preference_id: int) -> Sequence[ListingPreference]:
        """
        Retrieves all listing preferences associated with a given job preference.

        Args:
            preference_id (int): ID of the job preference.

        Returns:
            Sequence[ListingPreference]: All matching listing preferences.
        """
        async with async_session() as session:
            stmt = (
                select(ListingPreference)
                .where(ListingPreference.job_preference_id == preference_id)
            )
            result = await session.execute(stmt)
            return result.scalars().all()

    async def get_all_by_listing_id(self, job_id: int) -> Sequence[ListingPreference]:
        """
        Retrieves all listing preferences associated with a given job listing.

        Args:
            job_id (int): ID of the job listing.

        Returns:
            Sequence[ListingPreference]: All matching listing preferences.
        """
        async with async_session() as session:
            stmt = (
                select(ListingPreference)
                .where(ListingPreference.job_listing_id == job_id)
            )
            result = await session.execute(stmt)
            return result.scalars().all()

    async def get_all_unseen_by_preference_id(self, preference_id: int) -> Sequence[ListingPreference]:
        """
        Retrieves all listing preferences that have not yet been seen by the user.

        Args:
            preference_id (int): ID of the job preference.

        Returns:
            Sequence[ListingPreference]: All unseen listing preferences for the given preference.
        """
        async with async_session() as session:
            stmt = (
                select(ListingPreference)
                .where(
                    ListingPreference.job_preference_id == preference_id,
                    ListingPreference.is_seen == False
                )
            )
            result = await session.execute(stmt)
            return result.scalars().all()

    async def get_by_preference_id_and_listing_id(
        self,
        preference_id: int,
        listing_id: int,
    ) -> ListingPreference | None:
        """
        Retrieves a single listing-preference association for a given job preference and listing.

        Args:
            preference_id (int): ID of the job preference.
            listing_id (int): ID of the job listing.

        Returns:
            ListingPreference | None: The association if found, otherwise None.
        """
        async with async_session() as session:
            stmt = (
                select(ListingPreference)
                .where(
                    ListingPreference.job_preference_id == preference_id,
                    ListingPreference.job_listing_id == listing_id,
                )
            )
            result = await session.execute(stmt)
            return result.scalar_one_or_none()


# Singleton instance for accessing listing preference data
listing_preference_repository = ListingPreferenceRepository()