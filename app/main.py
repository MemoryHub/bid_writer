from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.user import router as user_router
from app.api.stamp import router as stamp_router
from app.db.database import engine, Base
from app.api import upload  # 确保导入 upload 路由

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

# 提供静态文件服务
app.mount("/resources", StaticFiles(directory="resources"), name="resources")

# 注册路由
app.include_router(user_router)
app.include_router(stamp_router)
app.include_router(upload.router)  # 添加 upload 路由
