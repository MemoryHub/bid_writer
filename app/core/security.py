from typing import Dict, Optional
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, IntegerIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_async_session, async_session
from app.models.user import User
from app.core.config import settings
from app.services.email_service import send_verification_email
from fastapi_users.password import PasswordHelper

# #################################################################
# #################### 用户管理器配置 #################################
# #################################################################

class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """用户管理器，处理用户注册、验证等操作"""
    
    # 用于密码重置和验证的密钥
    reset_password_token_secret = settings.SECRET_KEY
    verification_token_secret = settings.SECRET_KEY

    async def update(self, user: User, user_update: Dict):
        """更新用户"""
        if "password" in user_update:
            # 使用 PasswordHelper 来哈希新密码
            user.hashed_password = PasswordHelper().hash(user_update["password"])
        
        # 获取异步数据库会话
        session = await async_session()  # 获取会话

        # 如果 user 对象已经附加到其他会话中，我们需要合并它到当前会话
        user = await session.merge(user)  # 合并对象到当前会话

        session.add(user)  # 将修改过的用户添加到会话中
        await session.commit()  # 提交事务
        return user

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        """用户注册后的回调函数"""
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        """忘记密码后的回调函数"""
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        """请求验证后的回调函数"""
        print(f"Verification requested for user {user.id}. Verification token: {token}")

# #################################################################
# #################### 依赖项配置 ####################################
# #################################################################

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """获取用户数据库会话"""
    yield SQLAlchemyUserDatabase(session, User)

async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    """获取用户管理器实例"""
    yield UserManager(user_db)

# #################################################################
# #################### JWT认证配置 ##################################
# #################################################################

# 配置Bearer token传输
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    """获取JWT策略配置"""
    return JWTStrategy(secret=settings.SECRET_KEY, lifetime_seconds=3600)

# 配置认证后端
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

# 创建FastAPI Users实例
fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

# 获取当前活跃用户的依赖项
current_active_user = fastapi_users.current_user(active=True) 