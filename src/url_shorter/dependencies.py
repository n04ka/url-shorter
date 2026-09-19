from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Annotated
from .repos.repo import LinkRepo
from redis.asyncio import BlockingConnectionPool, Redis
from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlmodel import SQLModel
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from .config import config


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP (выполняется при запуске) ---
    print("🚀 Starting application...")

    # Инициализация Redis
    pool = BlockingConnectionPool.from_url(
        str(config.redis_url),
        max_connections=10,
    )
    global redis_client
    redis_client = Redis(connection_pool=pool)
    await redis_client.ping()  # Проверка соединения
    print("✅ Redis connected")
    FastAPICache.init(RedisBackend(redis_client), prefix="ural-shproter")

    # Инициализация БД
    global engine
    engine = create_async_engine(str(config.database_url))
    from .repos.models import Link  # type: ignore

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    print("✅ Database connected and tables created")

    yield  # Приложение работает здесь

    # --- SHUTDOWN (выполняется при остановке) ---
    print("🛑 Shutting down application...")

    await FastAPICache.clear()
    # Закрытие Redis
    if redis_client:
        await redis_client.close()
        print("✅ Redis disconnected")

    # Закрытие БД
    if engine:
        await engine.dispose()
        print("✅ Database disconnected")

    print("👋 Application stopped")


async def get_session() -> AsyncIterator[AsyncSession]:
    async with AsyncSession(engine) as session:
        yield session


async def get_cache() -> Redis:
    return redis_client


DB = Annotated[AsyncSession, Depends(get_session)]
CACHE = Annotated[Redis, Depends(get_cache)]


async def get_link_repo(session: DB) -> LinkRepo:
    return LinkRepo(session)


LINK_REPO = Annotated[LinkRepo, Depends(get_link_repo)]
