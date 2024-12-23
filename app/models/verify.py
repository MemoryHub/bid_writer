from pydantic import BaseModel, EmailStr
from app.schemas.user import UserCreate

# #################################################################
# #################### 验证相关模型 ##################################
# #################################################################

class EmailVerificationRequest(BaseModel):
    """邮箱验证请求模型"""
    email: EmailStr

class VerificationCodeRequest(BaseModel):
    """验证码验证请求模型"""
    email: EmailStr           # 邮箱地址
    code: str                 # 验证码
    user_create: UserCreate   # 用户创建信息

class PasswordResetRequest(BaseModel):
    """密码重置请求模型"""
    email: EmailStr       # 邮箱地址
    code: str            # 验证码
    new_password: str    # 新密码 