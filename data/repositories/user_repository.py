from data.models.user import User
from data.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    async def get_user_lang(self, id: int) -> str:
        user = await self.get_by_id(id)
        return user.language_code if user else "en"

user_repository = UserRepository()