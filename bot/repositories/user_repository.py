from bot.models.user import User
from bot.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

user_repository = UserRepository()