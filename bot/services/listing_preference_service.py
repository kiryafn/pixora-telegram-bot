from typing import Sequence

from bot.models import ListingPreference
from bot.repositories import ListingPreferenceRepository, listing_preference_repository
from bot.services import BaseService


class ListingPreferenceService(BaseService[ListingPreference]):
    """
    Service layer for managing ListingPreference entities.

    Handles the logic of linking job listings to user preferences and
    retrieving those associations with support for filtering unseen entries.

    Attributes:
        repository (ListingPreferenceRepository): The repository for ListingPreference entities.
    """

    repository: ListingPreferenceRepository

    def __init__(self, repository: ListingPreferenceRepository) -> None:
        """
        Initializes the service with a ListingPreference repository.

        Args:
            repository (ListingPreferenceRepository): The repository instance.
        """
        super().__init__(repository)

    async def link(self, listing_id: int, preference_id: int) -> ListingPreference:
        """
        Links a job listing to a job preference, if not already linked.

        If a link already exists, returns it instead of creating a new one.

        Args:
            listing_id (int): ID of the job listing.
            preference_id (int): ID of the job preference.

        Returns:
            ListingPreference: The existing or newly created association.
        """
        existing = await self.repository.get_by_preference_id_and_listing_id(
            preference_id,
            listing_id
        )

        if existing:
            return existing

        new_link = ListingPreference(
            job_listing_id=listing_id,
            job_preference_id=preference_id,
            is_seen=False,
        )
        return await self.repository.save(new_link)

    async def get_all_by_preference_id(self, preference_id: int) -> Sequence[ListingPreference]:
        """
        Retrieves all listing preferences linked to a specific job preference.

        Args:
            preference_id (int): The ID of the job preference.

        Returns:
            Sequence[ListingPreference]: List of listing-preference associations.
        """
        return await self.repository.get_all_by_preference_id(preference_id)

    async def get_all_by_job_id(self, job_id: int) -> Sequence[ListingPreference]:
        """
        Retrieves all listing preferences linked to a specific job listing.

        Args:
            job_id (int): The ID of the job listing.

        Returns:
            Sequence[ListingPreference]: List of listing-preference associations.
        """
        return await self.repository.get_all_by_listing_id(job_id)

    async def get_all_unseen_by_preference_id(self, preference_id: int) -> Sequence[ListingPreference]:
        """
        Retrieves all listing preferences for a given preference that haven't been seen.

        Args:
            preference_id (int): The ID of the job preference.

        Returns:
            Sequence[ListingPreference]: List of unseen associations.
        """
        return await self.repository.get_all_unseen_by_preference_id(preference_id)


# Singleton instance for accessing listing preference logic
listing_preference_service = ListingPreferenceService(listing_preference_repository)