from bot.models import User
from bot.repositories.user_repository import UserRepository, user_repository
from bot.services import BaseService


class UserService(BaseService[User]):
    def __init__(self, repository: UserRepository) -> None:
        super().__init__(repository)

user_service = UserService(user_repository)