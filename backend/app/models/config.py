"""
配置管理模型
用于在数据库中存储用户配置（如API Key等敏感信息）
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from cryptography.fernet import Fernet
import os

Base = declarative_base()


class SystemConfig(Base):
    """系统配置表 - 存储API Key等敏感配置"""
    __tablename__ = "system_config"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, index=True, nullable=False)
    value = Column(Text, nullable=True)  # 加密存储
    encrypted = Column(Boolean, default=True)
    description = Column(String(500))
    category = Column(String(50))  # ai, datasource, payment等
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<SystemConfig(key={self.key}, category={self.category})>"


class UserConfig(Base):
    """用户配置表 - 每个用户可以有自己的配置"""
    __tablename__ = "user_config"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    key = Column(String(100), nullable=False)
    value = Column(Text, nullable=True)
    encrypted = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<UserConfig(user_id={self.user_id}, key={self.key})>"


# 加密工具类
class ConfigEncryption:
    """配置加密/解密工具"""

    def __init__(self):
        # 从环境变量获取加密密钥，如果没有则生成一个
        encryption_key = os.getenv("CONFIG_ENCRYPTION_KEY")
        if not encryption_key:
            # 生成一个新密钥（生产环境应该从安全的地方获取）
            encryption_key = Fernet.generate_key().decode()

        self.cipher = Fernet(encryption_key.encode() if isinstance(encryption_key, str) else encryption_key)

    def encrypt(self, plain_text: str) -> str:
        """加密"""
        if not plain_text:
            return ""
        return self.cipher.encrypt(plain_text.encode()).decode()

    def decrypt(self, encrypted_text: str) -> str:
        """解密"""
        if not encrypted_text:
            return ""
        return self.cipher.decrypt(encrypted_text.encode()).decode()


# 全局加密实例
encryptor = ConfigEncryption()
