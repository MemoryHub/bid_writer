from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.user import router as user_router
from app.db.database import engine, Base

app = FastAPI(
    title="FastAPI Users Demo",
    description="FastAPI Users management example",
    version="1.0.0"
)

# 创建数据库表
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(user_router)
