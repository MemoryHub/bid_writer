from typing import Dict
from datetime import datetime, timedelta

# 简单的内存存储，实际应用中应该使用Redis或数据库
verification_codes: Dict[str, tuple[str, datetime]] = {}

def save_verification_code(email: str, code: str, expire_minutes: int = 5):
    """保存验证码"""
    expire_time = datetime.now() + timedelta(minutes=expire_minutes)
    verification_codes[email] = (code, expire_time)

def verify_code(email: str, code: str) -> bool:
    """验证验证码"""
    if email not in verification_codes:
        print(f"验证码未找到: {email}")
        return False
    saved_code, expire_time = verification_codes[email]
    if datetime.now() > expire_time:
        del verification_codes[email]
        print(f"验证码已过期: {email}")
        return False
    if code != saved_code:
        print(f"验证码不匹配: {code} != {saved_code}")
        return False
    del verification_codes[email]  # 使用后删除验证码
    return True 