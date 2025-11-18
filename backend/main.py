"""
AI选品系统 - 主应用入口
"""

import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from loguru import logger
import sys

from app.core.config import settings
from app.api.v1 import api_router


# 配置日志
logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level=settings.LOG_LEVEL
)
logger.add(
    settings.LOG_FILE,
    rotation=settings.LOG_ROTATION,
    retention=settings.LOG_RETENTION,
    level=settings.LOG_LEVEL
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    logger.info("🚀 应用启动中...")
    logger.info(f"📦 应用名称: {settings.APP_NAME}")
    logger.info(f"🔢 版本号: {settings.APP_VERSION}")
    logger.info(f"🐛 调试模式: {settings.DEBUG}")
    logger.info(f"🗄️  数据库: {settings.DATABASE_URL.split('@')[-1] if '@' in settings.DATABASE_URL else 'N/A'}")

    # 这里可以添加启动任务
    # 例如: 初始化数据库连接池、启动定时任务等

    yield

    # 关闭时执行
    logger.info("👋 应用关闭中...")
    # 这里可以添加清理任务


# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    description="""
    ## AI选品系统 - TikTok美国站

    ### 核心功能
    - ✅ 自动采集8大数据源
    - ✅ AI智能分析产品潜力
    - ✅ 自动评分（100分制）
    - ✅ 自动生成爆款脚本
    - ✅ 自动推荐供应商
    - ✅ 持续监控和预警

    ### 使用流程
    1. 输入产品关键词或1688链接
    2. 系统自动分析（5-10分钟）
    3. 查看评估报告
    4. 做出决策

    ### API文档
    - Swagger UI: `/docs`
    - ReDoc: `/redoc`
    """,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except RuntimeError:
    logger.warning("⚠️  静态文件目录不存在，跳过挂载")

# 挂载API路由
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


# 根路由
@app.get("/", tags=["Root"])
async def root():
    """根路径 - 系统信息"""
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc",
        "api_v1": settings.API_V1_PREFIX
    }


# 健康检查
@app.get("/health", tags=["Health"])
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION
    }


# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """全局异常处理"""
    logger.error(f"❌ 全局异常: {exc}")
    logger.exception(exc)

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc) if settings.DEBUG else "An error occurred",
            "type": type(exc).__name__
        }
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
