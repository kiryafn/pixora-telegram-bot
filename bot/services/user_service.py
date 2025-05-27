from bot.models import User
from bot.repositories import UserRepository, user_repository
from bot.services import BaseService


class UserService(BaseService[User]):
    def __init__(self, repository: UserRepository) -> None:
        super().__init__(repository)

    async def get_user_lang(self, id):
        return await user_repository.get_user_lang(id)

    async def get_all_active(self) -> User | None:
        return await user_repository.get_all_active()


user_service = UserService(user_repository)