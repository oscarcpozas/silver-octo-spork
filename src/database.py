from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import get_settings

engine = create_async_engine(get_settings().database_url, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
