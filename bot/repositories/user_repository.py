from sqlalchemy import select

from bot.configuration.database import async_session
from bot.models import User
from bot.repositories import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self) -> None:
        super().__init__(User)

    #todo possibly replace by get_by_id(id).language
    async def get_user_lang(self, id):
        user = await self.get_by_id(id)
        return user.language

    async def get_all_active(self) -> list[User]:
        async with async_session() as session:
            stmt = select(User).where(User.is_active.is_(True))
            result = await session.execute(stmt)
            return result.scalars().all()

user_repository = UserRepository()