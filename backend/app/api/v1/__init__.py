"""API v1 路由"""

from fastapi import APIRouter
from .endpoints import products, config

api_router = APIRouter()

# 注册路由
api_router.include_router(
    products.router,
    prefix="/products",
    tags=["Products - 产品分析"]
)

api_router.include_router(
    config.router,
    prefix="/config",
    tags=["Config - 配置管理"]
)


# 欢迎路由
@api_router.get("/", summary="API首页")
async def api_home():
    """API v1 首页"""
    return {
        "message": "🎉 AI选品系统 API v1",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "products": {
                "analyze": "POST /api/v1/products/analyze - 完整产品分析",
                "quick_score": "POST /api/v1/products/quick-score - 快速评分",
                "batch_analyze": "POST /api/v1/products/batch-analyze - 批量分析",
                "demo": "GET /api/v1/products/demo - 演示分析"
            },
            "config": {
                "status": "GET /api/v1/config/status - 配置状态",
                "set_api_keys": "POST /api/v1/config/api-keys - 配置API Keys",
                "set_system": "POST /api/v1/config/system - 系统设置"
            }
        },
        "docs": "/docs",
        "tips": "💡 首次使用，请先访问 /api/v1/config/status 查看配置状态"
    }
