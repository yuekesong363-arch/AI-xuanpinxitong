"""
配置管理服务
处理API Key等敏感配置的存储和读取
"""

from typing import Optional, Dict, Any
from loguru import logger


class ConfigService:
    """配置服务 - 管理API Key等配置"""

    def __init__(self):
        self._config_cache: Dict[str, Any] = {}
        self._load_default_config()

    def _load_default_config(self):
        """加载默认配置"""
        self._config_cache = {
            # AI服务配置
            "openai_api_key": None,
            "openai_model": "gpt-4-vision-preview",
            "openai_text_model": "gpt-4-turbo-preview",
            "anthropic_api_key": None,

            # 数据源配置
            "google_trends_api_key": None,
            "use_proxy": False,
            "proxy_url": None,

            # 系统配置
            "use_mock_data": True,  # 默认使用Mock数据
            "skip_ai_analysis": True,  # 默认跳过AI分析
            "skip_scraping": True,  # 默认跳过爬虫
        }

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置"""
        value = self._config_cache.get(key, default)
        logger.debug(f"📖 获取配置: {key} = {value if key != 'openai_api_key' else '***'}")
        return value

    def set(self, key: str, value: Any) -> None:
        """设置配置"""
        self._config_cache[key] = value
        logger.info(f"💾 设置配置: {key} = {value if 'key' not in key.lower() else '***'}")

        # 自动调整相关配置
        self._auto_adjust_config(key, value)

    def _auto_adjust_config(self, key: str, value: Any):
        """自动调整相关配置"""
        # 如果设置了OpenAI API Key，自动启用真实AI分析
        if key == "openai_api_key" and value:
            self._config_cache["skip_ai_analysis"] = False
            self._config_cache["use_mock_data"] = False
            logger.info("✅ 检测到OpenAI API Key，自动启用真实AI分析")

    def set_batch(self, configs: Dict[str, Any]) -> None:
        """批量设置配置"""
        for key, value in configs.items():
            self.set(key, value)

    def get_all(self) -> Dict[str, Any]:
        """获取所有配置（隐藏敏感信息）"""
        safe_config = {}
        for key, value in self._config_cache.items():
            if "key" in key.lower() or "password" in key.lower():
                safe_config[key] = "***" if value else None
            else:
                safe_config[key] = value
        return safe_config

    def has_openai_key(self) -> bool:
        """检查是否配置了OpenAI API Key"""
        return bool(self._config_cache.get("openai_api_key"))

    def should_use_mock(self) -> bool:
        """是否应该使用Mock数据"""
        return self._config_cache.get("use_mock_data", True)

    def should_skip_ai(self) -> bool:
        """是否应该跳过AI分析"""
        return self._config_cache.get("skip_ai_analysis", True)

    def should_skip_scraping(self) -> bool:
        """是否应该跳过爬虫"""
        return self._config_cache.get("skip_scraping", True)

    def validate_config(self) -> Dict[str, bool]:
        """验证配置完整性"""
        return {
            "openai_configured": self.has_openai_key(),
            "can_use_ai": not self.should_skip_ai(),
            "can_scrape": not self.should_skip_scraping(),
            "using_mock": self.should_use_mock(),
        }


# 全局配置服务实例
config_service = ConfigService()
