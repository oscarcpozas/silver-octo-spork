from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Lazy-initialized — get_settings() is NOT called at import time.
# First call to async_session() or get_db_session() triggers initialization.
_session_factory: async_sessionmaker | None = None


def _get_session_factory() -> async_sessionmaker:
    global _session_factory
    if _session_factory is None:
        from src.config import get_settings
        engine = create_async_engine(get_settings().database_url, echo=False)
        _session_factory = async_sessionmaker(engine, expire_on_commit=False)
    return _session_factory


def async_session() -> AsyncSession:
    """Return a new AsyncSession. Used by background scheduler tasks."""
    return _get_session_factory()()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields a managed AsyncSession."""
    async with _get_session_factory()() as session:
        yield session
