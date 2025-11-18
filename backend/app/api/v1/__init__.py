"""API v1 路由"""

from fastapi import APIRouter

# 导入各个端点路由
# from .endpoints import products, analysis, discover, monitor, scripts, suppliers

api_router = APIRouter()

# 注册路由（暂时注释，等实现后再取消注释）
# api_router.include_router(products.router, prefix="/products", tags=["Products"])
# api_router.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])
# api_router.include_router(discover.router, prefix="/discover", tags=["Discover"])
# api_router.include_router(monitor.router, prefix="/monitor", tags=["Monitor"])
# api_router.include_router(scripts.router, prefix="/scripts", tags=["Scripts"])
# api_router.include_router(suppliers.router, prefix="/suppliers", tags=["Suppliers"])


# 临时测试路由
@api_router.get("/test")
async def test_api():
    """API测试端点"""
    return {
        "message": "API v1 is working!",
        "status": "success"
    }
