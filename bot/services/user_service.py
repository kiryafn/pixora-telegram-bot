from bot.models import User
from bot.repositories import UserRepository, user_repository
from bot.services import BaseService


class UserService(BaseService[User]):
    """
    Service layer for managing User entities.

    Extends BaseService with user-specific methods such as retrieving
    language preferences and listing all active users.
    """

    repository: UserRepository

    def __init__(self, repository: UserRepository) -> None:
        """
        Initializes the UserService with a UserRepository.

        Args:
            repository (UserRepository): The repository for user data access.
        """
        super().__init__(repository)

    async def get_user_lang(self, id: int) -> str:
        """
        Retrieves the preferred language of a user by their ID.

        Args:
            id (int): The user's ID.

        Returns:
            str: The user's preferred language code (e.g., 'en', 'pl').
        """
        return await self.repository.get_user_lang(id)

    async def get_all_active(self) -> list[User]:
        """
        Retrieves all users that are marked as active.

        Returns:
            list[User]: A list of active users.
        """
        return await self.repository.get_all_active()


# Singleton instance for accessing user-related logic
user_service = UserService(user_repository)