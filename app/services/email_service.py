from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from app.core.config import settings
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)

# #################################################################
# #################### 邮件服务配置 ##################################
# #################################################################

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_TLS,
    MAIL_SSL_TLS=settings.MAIL_SSL,
    USE_CREDENTIALS=True,
)

# #################################################################
# #################### 邮件发送功能 ##################################
# #################################################################

async def send_verification_email(email: EmailStr, verification_code: str):
    """
    发送验证码邮件
    Args:
        email: 目标邮箱地址
        verification_code: 验证码
    """
    message = MessageSchema(
        subject="邮箱验证",
        recipients=[email],
        body=f"你的验证码是: {verification_code}",
        subtype="html"
    )
    
    fm = FastMail(conf)
    await fm.send_message(message)

async def send_reset_password_email(email: EmailStr, verification_code: str):
    """
    发送密码重置验证码邮件
    Args:
        email: 目标邮箱地址
        verification_code: 验证码
    """
    message = MessageSchema(
        subject="重置密码",
        recipients=[email],
        body=f"你重置密码操作的验证码是: {verification_code}",
        subtype="html"
    )
    
    fm = FastMail(conf)
    await fm.send_message(message) 