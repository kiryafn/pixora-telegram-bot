from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from bot.models.user import User
from typing import Optional


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def get_user_by_id(self, user_id: int) -> User | None:
        stmt = (
            select(User)
            .where(User.id == user_id)
        )
        result: Result = await self.session.execute(stmt)
        user: Optional[User] = result.scalar_one_or_none()
        return user

    async def create_user(self, user_id: int, username: str, language: str) -> User:
        user: User = User(id=user_id, username=username, language=language)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update_user(self, user_id: int, username: str, language: str) -> User | None:
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(username=username, language=language)
        )
        await self.session.execute(stmt)
        await self.session.commit()
        updated_user: Optional[User] = await self.get_user_by_id(user_id)
        return updated_user