import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.verify_service import save_verification_code

client = TestClient(app)

def test_send_registration_code():
    """测试发送注册验证码"""
    response = client.post(
        "/auth/register/send-code",
        json={"email": "test@example.com"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "验证码已发送"

def test_register_with_code():
    """测试使用验证码注册"""
    # 模拟保存验证码
    test_email = "test@example.com"
    test_code = "123456"
    save_verification_code(test_email, test_code)
    
    response = client.post(
        "/auth/register/verify",
        json={
            "email": test_email,
            "code": test_code,
            "user_create": {
                "email": test_email,
                "password": "testpassword123"
            }
        }
    )
    assert response.status_code == 200
    assert response.json()["message"] == "注册成功"

def test_login():
    """测试用户登���"""
    response = client.post(
        "/auth/jwt/login",
        data={
            "username": "test@example.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_send_reset_password_code():
    """测试发送重置密码验证码"""
    response = client.post(
        "/auth/forgot-password/send-code",
        json={"email": "test@example.com"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Reset password code sent"

def test_reset_password():
    """测试重置密码"""
    # 模拟保存验证码
    test_email = "test@example.com"
    test_code = "123456"
    save_verification_code(test_email, test_code)
    
    response = client.post(
        "/auth/reset-password/verify",
        json={
            "email": test_email,
            "code": test_code,
            "new_password": "newpassword123"
        }
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Password reset successful"

def test_invalid_verification_code():
    """测试无效的验证码"""
    response = client.post(
        "/auth/register/verify",
        json={
            "email": "test@example.com",
            "code": "000000",  # 错误的验证码
            "user_create": {
                "email": "test@example.com",
                "password": "testpassword123"
            }
        }
    )
    assert response.status_code == 400
    assert "无效的验证码" in response.json()["detail"] 