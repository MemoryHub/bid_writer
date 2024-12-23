from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

# 创建异步引擎
engine = create_async_engine(settings.DATABASE_URL)

# 创建异步会话
async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# 创建 Base 类
Base = declarative_base()

# 获取异步数据库会话
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session 

# 获取异步数据库会话
async def async_session() -> AsyncSession:
    async with async_session_maker() as session:
        return session  # 直接返回会话对象