"""
应用配置
使用 pydantic-settings 管理配置
"""

from typing import List, Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # ==========================================
    # 应用配置
    # ==========================================
    APP_NAME: str = "AI选品系统"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    SECRET_KEY: str = Field(..., min_length=32)

    # API配置
    API_V1_PREFIX: str = "/api/v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # ==========================================
    # 数据库配置
    # ==========================================
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10

    REDIS_URL: str
    REDIS_PASSWORD: Optional[str] = None

    MONGODB_URL: str
    MONGODB_DB_NAME: str = "xuanpin"

    # ==========================================
    # AI配置
    # ==========================================
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4-vision-preview"
    OPENAI_TEXT_MODEL: str = "gpt-4-turbo-preview"

    ANTHROPIC_API_KEY: Optional[str] = None

    # ==========================================
    # 爬虫配置
    # ==========================================
    USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    SCRAPER_TIMEOUT: int = 30
    SCRAPER_MAX_RETRIES: int = 3

    HTTP_PROXY: Optional[str] = None
    HTTPS_PROXY: Optional[str] = None
    SOCKS_PROXY: Optional[str] = None

    # ==========================================
    # 任务队列配置
    # ==========================================
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # ==========================================
    # 监控配置
    # ==========================================
    AUTO_DISCOVER_TIME: str = "01:00"
    MONITORING_INTERVAL: int = 24  # 小时
    ALERT_VIDEO_GROWTH_THRESHOLD: int = 50  # %
    ALERT_SALES_GROWTH_THRESHOLD: int = 100  # %

    # ==========================================
    # 存储配置
    # ==========================================
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    IMAGE_STORAGE_TYPE: str = "local"
    IMAGE_BASE_URL: str = "http://localhost:8000/static/images"

    # S3配置
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_S3_BUCKET: Optional[str] = None
    AWS_S3_REGION: str = "us-east-1"

    # ==========================================
    # 评分配置
    # ==========================================
    WEIGHT_MARKET_DEMAND: int = 10
    WEIGHT_FUNCTIONAL_VALUE: int = 10
    WEIGHT_EMOTIONAL_VALUE: int = 10
    WEIGHT_CONTENT_VALUE: int = 15
    WEIGHT_PLEASURE_PAIN: int = 10
    WEIGHT_US_MARKET_FIT: int = 10
    WEIGHT_SIZE_LOGISTICS: int = 10
    WEIGHT_COMPETITION: int = 10
    WEIGHT_SUPPLY_PRICING: int = 15

    SCORE_S_THRESHOLD: int = 85
    SCORE_A_THRESHOLD: int = 75
    SCORE_B_THRESHOLD: int = 65
    SCORE_C_THRESHOLD: int = 55

    # ==========================================
    # 利润计算配置
    # ==========================================
    DEFAULT_PLATFORM_FEE_RATE: float = 0.15
    DEFAULT_AD_COST_RATE: float = 0.20
    DEFAULT_RETURN_RATE: float = 0.04
    DEFAULT_PACKAGING_COST: float = 0.50

    SHIPPING_COST_PER_KG: float = 8.00
    WAREHOUSE_FEE_SMALL: float = 0.80
    WAREHOUSE_FEE_MEDIUM: float = 1.50
    WAREHOUSE_FEE_LARGE: float = 3.00

    CNY_TO_USD_RATE: float = 0.14

    # ==========================================
    # 限流配置
    # ==========================================
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 60

    # ==========================================
    # CORS配置
    # ==========================================
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: str = "*"
    CORS_ALLOW_HEADERS: str = "*"

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: str) -> List[str]:
        """解析CORS origins"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    # ==========================================
    # 日志配置
    # ==========================================
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/app.log"
    LOG_ROTATION: str = "500 MB"
    LOG_RETENTION: str = "30 days"

    # ==========================================
    # 安全配置
    # ==========================================
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    PASSWORD_BCRYPT_ROUNDS: int = 12

    # ==========================================
    # 缓存配置
    # ==========================================
    CACHE_DEFAULT_TTL: int = 3600
    CACHE_ANALYSIS_TTL: int = 86400
    CACHE_TRENDS_TTL: int = 3600

    # ==========================================
    # 开发配置
    # ==========================================
    USE_MOCK_DATA: bool = False
    SKIP_SCRAPING: bool = False
    SKIP_AI_ANALYSIS: bool = False

    # ==========================================
    # 计算属性
    # ==========================================
    @property
    def async_database_url(self) -> str:
        """异步数据库URL"""
        return self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

    @property
    def cors_origins_list(self) -> List[str]:
        """CORS origins列表"""
        if isinstance(self.CORS_ORIGINS, str):
            return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
        return self.CORS_ORIGINS

    def calculate_grade(self, score: float) -> str:
        """根据分数计算等级"""
        if score >= self.SCORE_S_THRESHOLD:
            return "S"
        elif score >= self.SCORE_A_THRESHOLD:
            return "A"
        elif score >= self.SCORE_B_THRESHOLD:
            return "B"
        elif score >= self.SCORE_C_THRESHOLD:
            return "C"
        else:
            return "D"

    def get_recommendation_by_score(self, score: float) -> dict:
        """根据分数获取推荐"""
        grade = self.calculate_grade(score)

        recommendations = {
            "S": {
                "action": "immediate_test",
                "priority": "critical",
                "message": "立即测试，优先分配资源"
            },
            "A": {
                "action": "priority_test",
                "priority": "high",
                "message": "重点测试"
            },
            "B": {
                "action": "small_test",
                "priority": "medium",
                "message": "小额测试"
            },
            "C": {
                "action": "consider",
                "priority": "low",
                "message": "谨慎考虑"
            },
            "D": {
                "action": "pass",
                "priority": "none",
                "message": "不建议"
            }
        }

        return recommendations.get(grade, recommendations["D"])


# 创建全局配置实例
settings = Settings()


# 导出配置
__all__ = ["settings", "Settings"]
