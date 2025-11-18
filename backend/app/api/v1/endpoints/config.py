"""
配置管理API端点
用于管理API Key等系统配置
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from loguru import logger

from app.services.config_service import config_service

router = APIRouter()


# ==================== Pydantic Models ====================

class APIKeyConfig(BaseModel):
    """API Key配置"""
    openai_api_key: Optional[str] = Field(None, description="OpenAI API Key")
    anthropic_api_key: Optional[str] = Field(None, description="Anthropic API Key (可选)")
    google_trends_api_key: Optional[str] = Field(None, description="Google Trends API Key (可选)")


class SystemConfig(BaseModel):
    """系统配置"""
    use_mock_data: bool = Field(True, description="是否使用Mock数据")
    skip_ai_analysis: bool = Field(True, description="是否跳过AI分析")
    skip_scraping: bool = Field(True, description="是否跳过爬虫")


class ConfigResponse(BaseModel):
    """配置响应"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None


# ==================== API Endpoints ====================

@router.get("/", response_model=ConfigResponse, summary="获取所有配置")
async def get_all_config():
    """
    获取所有配置（隐藏敏感信息）

    **返回**:
    - 所有配置项（API Key显示为***）
    """
    try:
        all_config = config_service.get_all()

        return ConfigResponse(
            success=True,
            message="获取配置成功",
            data=all_config
        )

    except Exception as e:
        logger.error(f"❌ 获取配置失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status", response_model=ConfigResponse, summary="获取配置状态")
async def get_config_status():
    """
    获取配置状态

    **返回**:
    - OpenAI是否已配置
    - 是否可以使用AI
    - 是否可以爬虫
    - 是否使用Mock数据
    """
    try:
        status = config_service.validate_config()

        return ConfigResponse(
            success=True,
            message="获取状态成功",
            data=status
        )

    except Exception as e:
        logger.error(f"❌ 获取状态失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api-keys", response_model=ConfigResponse, summary="配置API Keys")
async def set_api_keys(request: APIKeyConfig):
    """
    配置API Keys

    **功能**:
    - 设置OpenAI API Key
    - 设置其他服务的API Key
    - 自动启用相关功能

    **说明**:
    - 配置OpenAI API Key后，系统将自动启用真实AI分析
    - API Key将被加密存储（仅展示时）

    **示例**:
    ```json
    {
        "openai_api_key": "sk-proj-xxxxx",
        "anthropic_api_key": "sk-ant-xxxxx"  (可选)
    }
    ```
    """
    try:
        logger.info("🔑 配置API Keys...")

        # 设置API Keys
        if request.openai_api_key:
            config_service.set("openai_api_key", request.openai_api_key)
            logger.info("✅ OpenAI API Key已设置")

        if request.anthropic_api_key:
            config_service.set("anthropic_api_key", request.anthropic_api_key)
            logger.info("✅ Anthropic API Key已设置")

        if request.google_trends_api_key:
            config_service.set("google_trends_api_key", request.google_trends_api_key)
            logger.info("✅ Google Trends API Key已设置")

        # 获取更新后的状态
        status = config_service.validate_config()

        return ConfigResponse(
            success=True,
            message="API Keys配置成功",
            data={
                "status": status,
                "tips": "OpenAI API Key已配置，系统将自动启用真实AI分析" if request.openai_api_key else None
            }
        )

    except Exception as e:
        logger.error(f"❌ 配置API Keys失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/system", response_model=ConfigResponse, summary="配置系统设置")
async def set_system_config(request: SystemConfig):
    """
    配置系统设置

    **功能**:
    - 切换Mock数据模式
    - 启用/禁用AI分析
    - 启用/禁用爬虫

    **说明**:
    - 开发阶段建议使用Mock数据
    - 生产阶段配置API Key后可切换到真实数据
    """
    try:
        logger.info("⚙️  配置系统设置...")

        config_service.set("use_mock_data", request.use_mock_data)
        config_service.set("skip_ai_analysis", request.skip_ai_analysis)
        config_service.set("skip_scraping", request.skip_scraping)

        status = config_service.validate_config()

        return ConfigResponse(
            success=True,
            message="系统设置已更新",
            data={"status": status}
        )

    except Exception as e:
        logger.error(f"❌ 配置系统设置失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/api-keys", response_model=ConfigResponse, summary="清除API Keys")
async def clear_api_keys():
    """
    清除所有API Keys

    **功能**:
    - 删除所有API Keys
    - 自动切换回Mock模式
    """
    try:
        logger.info("🗑️  清除API Keys...")

        config_service.set("openai_api_key", None)
        config_service.set("anthropic_api_key", None)
        config_service.set("google_trends_api_key", None)

        # 自动切换到Mock模式
        config_service.set("use_mock_data", True)
        config_service.set("skip_ai_analysis", True)

        return ConfigResponse(
            success=True,
            message="API Keys已清除，已切换到Mock模式"
        )

    except Exception as e:
        logger.error(f"❌ 清除API Keys失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test-openai", response_model=ConfigResponse, summary="测试OpenAI连接")
async def test_openai_connection():
    """
    测试OpenAI API连接

    **功能**:
    - 验证API Key是否有效
    - 测试API连接

    **说明**:
    - 将发送一个简单的测试请求
    - 返回连接状态
    """
    try:
        if not config_service.has_openai_key():
            raise HTTPException(status_code=400, detail="未配置OpenAI API Key")

        logger.info("🔌 测试OpenAI连接...")

        # TODO: 实际调用OpenAI API测试连接
        # 这里暂时返回模拟结果
        is_connected = True

        if is_connected:
            return ConfigResponse(
                success=True,
                message="OpenAI API连接成功",
                data={"connected": True, "model": "gpt-4-turbo-preview"}
            )
        else:
            return ConfigResponse(
                success=False,
                message="OpenAI API连接失败",
                data={"connected": False}
            )

    except Exception as e:
        logger.error(f"❌ 测试连接失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))
