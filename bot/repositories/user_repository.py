from sqlalchemy import select

from bot.configuration.database import async_session
from bot.models import User
from bot.repositories import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    Repository for managing User entities.

    Extends BaseRepository with methods for retrieving user language preferences
    and filtering active users.
    """

    def __init__(self) -> None:
        """
        Initializes the repository with the User model.
        """
        super().__init__(User)

    # TODO: Possibly replace with direct use of get_by_id(id).language
    async def get_user_lang(self, id: int) -> str:
        """
        Retrieves the preferred language of a user by their ID.

        Args:
            id (int): The user's ID.

        Returns:
            str: The language code (e.g., 'en', 'pl').
        """
        user = await self.get_by_id(id)
        return str(user.language)

    async def get_all_active(self) -> list[User]:
        """
        Retrieves all users marked as active.

        Returns:
            list[User]: A list of active user records.
        """
        async with async_session() as session:
            stmt = select(User).where(User.is_active.is_(True))
            result = await session.execute(stmt)
            return result.scalars().all()


# Singleton instance for accessing user data
user_repository = UserRepository()