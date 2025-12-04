"""
配置文件 - XXXX协会科学技术奖评审管理系统
Configuration for XXXX Association Technology Award Management System
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """系统配置"""
    
    # 应用基础配置
    APP_NAME: str = "XXXX协会科学技术奖评审管理系统"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # 数据库配置
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = "root"
    DB_NAME: str = "nonferrous_award_system"
    
    # JWT 配置
    SECRET_KEY: str = "your-secret-key-change-in-production-nonferrous-award-2024"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24小时
    
    # 文件上传配置
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS: set = {".pdf", ".docx", ".doc", ".zip", ".png", ".jpg", ".jpeg"}
    
    # 邮件配置（占位）
    SMTP_HOST: Optional[str] = "smtp.example.com"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM: Optional[str] = None
    
    # CORS 配置
    CORS_ORIGINS: list = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ]
    
    # 分页配置
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    @property
    def DATABASE_URL(self) -> str:
        """生成数据库连接URL"""
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset=utf8mb4"
    
    
    model_config = {"env_file": ".env", "case_sensitive": True}


# 创建全局配置实例
settings = Settings()
