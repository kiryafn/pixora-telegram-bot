from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine, async_sessionmaker

from bot.configuration.config import settings

from sqlalchemy.orm import sessionmaker

engine: AsyncEngine = create_async_engine(
    settings.database_url,
    echo=True,
)

AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

async def create_db() -> None:
    from bot.models import Base

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)