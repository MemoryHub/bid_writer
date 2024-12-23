import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.database import Base, get_async_session

# 创建测试数据库连接
TEST_MYSQL_URL = "mysql+aiomysql://zhangbo:iDU6nyw2RGtU@578d7e0e5ca35.bj.cdb.myqcloud.com:3449/bid_writer"

engine = create_async_engine(
    TEST_MYSQL_URL,
    echo=True,
)

# 创建异步会话
TestingSessionLocal = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

@pytest.fixture
async def test_db():
    # 创建所有表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    try:
        async with TestingSessionLocal() as session:
            yield session
    finally:
        # 清理数据
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
def client(test_db):
    async def override_get_db():
        try:
            yield test_db
        finally:
            await test_db.close()
            
    app.dependency_overrides[get_async_session] = override_get_db
    return TestClient(app) 