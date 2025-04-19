from sqlalchemy import select
from bot.core.db import async_session
from bot.models.user import User

class UserRepository:

    @staticmethod
    async def get_by_id(user_id: int) -> User | None:
        async with async_session() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            return result.scalar_one_or_none()

    @staticmethod
    async def save(user: User) -> None:
        async with async_session() as session:
            session.add(user)
            await session.commit()