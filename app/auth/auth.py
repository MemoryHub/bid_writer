from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from app.models import User
from app.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
import secrets

# 生成一个 32 字节的随机密钥
SECRET_KEY = secrets.token_hex(32)  # 64 个字符，包含数字和字母

auth_backends = [
    JWTAuthentication(secret=SECRET_KEY, lifetime_seconds=3600)
]

# FastAPI Users 配置
fastapi_users = FastAPIUsers[User, int](
    get_user_db=get_db,
    auth_backends=auth_backends,
)
