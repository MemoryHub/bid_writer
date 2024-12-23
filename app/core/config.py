from pydantic_settings import BaseSettings
import secrets

def generate_secret_key() -> str:
    """生成随机密钥"""
    return secrets.token_hex(32)

class Settings(BaseSettings):
    """应用配置类，管理所有配置项"""
    # 核心配置
    SECRET_KEY: str = generate_secret_key()  # 动态生成密钥
    
    # 数据库配置
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_PORT: str
    MYSQL_DB: str

    @property
    def DATABASE_URL(self) -> str:
        """构建数据库URL"""
        return f"mysql+aiomysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"
    
    # 邮件服务配置
    MAIL_USERNAME: str = "bidwriter@xinoutech.com"    # 邮箱账号
    MAIL_PASSWORD: str = "youquer90AVENUE"            # 邮箱密码
    MAIL_FROM: str = "bidwriter@xinoutech.com"        # 发件人地址
    MAIL_PORT: int = 465                              # SMTP端口，使用SSL的端口
    MAIL_SERVER: str = "smtp.exmail.qq.com"           # 腾讯企业邮箱SMTP服务器
    MAIL_TLS: bool = False                            # 不使用TLS
    MAIL_SSL: bool = True                             # 使用SSL
    USE_CREDENTIALS: bool = True                      # 使用验证
    VALIDATE_CERTS: bool = True                       # 验证证书

    class Config:
        """配置类设置"""
        env_file = ".env"  # 从.env文件加载配置

settings = Settings()  # 创建配置实例 