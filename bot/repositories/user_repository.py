from bot.models.user import User
from bot.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self) -> None:
        super().__init__(User)

    async def get_user_lang(self, id):
        user = await self.get_by_id(id)
        print(user.language)
        return user.language

user_repository = UserRepository()