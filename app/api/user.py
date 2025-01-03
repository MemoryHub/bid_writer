from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import models
from fastapi_users.router.common import ErrorCode
from pydantic import EmailStr
import random
import string
from datetime import datetime

from app.core.security import fastapi_users, auth_backend, current_active_user
from app.services.email_service import send_verification_email, send_reset_password_email
from app.models.user import User
from app.models.verify import (
    EmailVerificationRequest,
    PasswordResetRequest,
    VerificationCodeRequest,
)
from app.services.verify_service import verify_code, save_verification_code
from app.models.response import ResponseModel

router = APIRouter(prefix="/auth", tags=["auth"])

# #################################################################
# #################### 验证码生成工具 ################################
# #################################################################

def generate_verification_code(length: int = 6) -> str:
    """生成指定长度的数字验证码"""
    return ''.join(random.choices(string.digits, k=length))

# #################################################################
# #################### 注册相关接口 ##################################
# #################################################################

# 1. 发送注册验证码
@router.post("/register/send-code", response_model=ResponseModel)
async def send_registration_code(email: EmailStr, user_manager=Depends(fastapi_users.get_user_manager),):
    """
    发送注册验证码
    1. 生成6位数字验证码
    2. 发送验证码到指定邮箱
    3. 将验证码保存到缓存或数据库中
    """
    
    # 检查邮箱是否已注册
    user = await user_manager.get_by_email(email)
    if user:
        return ResponseModel(code=1001, message="该邮箱已注册")

    verification_code = generate_verification_code()
    await send_verification_email(email, verification_code)
    save_verification_code(email, verification_code)
    return ResponseModel(code=200, message="验证码已发送")

# 2. 验证码注册
@router.post("/register/verify", response_model=ResponseModel)
async def verify_and_register(
    request: VerificationCodeRequest,
    user_manager=Depends(fastapi_users.get_user_manager),
):
    """
    验证码注册
    1. 验证邮箱验证码
    2. 创建新用户
    """
    if not verify_code(request.email, request.code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的验证码",
        )
    
    try:
        user = await user_manager.create(
            request.user_create,
            safe=True,
            request=None,
        )
        # 将 User 对象转换为字典并返回
        user_data = {
            "id": user.id,
            "email": user.email
        }
        return ResponseModel(code=200, message="注册成功", data=user_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

# #################################################################
# #################### 登录相关接口 ##################################
# #################################################################

# 3. 登录
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
)

# #################################################################
# #################### 密码重置相关接口 ##############################
# #################################################################

# 4. 发送重置密码验证码
@router.post("/forgot-password/send-code", response_model=ResponseModel)
async def send_reset_password_code(email: EmailStr):
    """发送密码重置验证码"""
    verification_code = generate_verification_code()  # 生成验证码
    await send_reset_password_email(email, verification_code)  # 发送邮件
    save_verification_code(email, verification_code)  # 保存验证码
    return ResponseModel(code=200, message="找回密码验证码已发送")

# 5. 重置密码
@router.post("/reset-password/verify", response_model=ResponseModel)
async def verify_and_reset_password(
    request: PasswordResetRequest,
    user_manager=Depends(fastapi_users.get_user_manager),
):    
    # 验证验证码
    if not verify_code(request.email, request.code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的验证码",
        )
    
    try:
        # 获取用户
        user = await user_manager.get_by_email(request.email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户未找到",
            )
        

        
        # 更新用户密码
        user_update = {"password": request.new_password}  # 创建更新字典
        await user_manager.update(user,user_update)  # 直接传递 user 实例

        return ResponseModel(code=200, message="密码修改成功")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) 

@router.post("/auth/jwt/logout", response_model=ResponseModel)
async def logout(user=Depends(current_active_user)):
    """登出用户"""
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户未登录")
    return ResponseModel(code=200, message="登出成功")