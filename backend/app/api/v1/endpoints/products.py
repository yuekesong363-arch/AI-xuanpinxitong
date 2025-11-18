"""
产品分析API端点
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from loguru import logger

from app.services.analysis_service import analysis_service

router = APIRouter()


# ==================== Pydantic Models ====================

class ProductAnalysisRequest(BaseModel):
    """产品分析请求"""
    product_name: str = Field(..., description="产品名称（英文）", example="Car Phone Holder")
    product_url: Optional[str] = Field(None, description="产品链接（1688等）")
    selling_price: Optional[float] = Field(None, description="预期售价(USD)", example=24.99, gt=0)
    purchase_price_cny: Optional[float] = Field(None, description="采购价(CNY)", example=20, gt=0)
    dimensions: Optional[Dict[str, float]] = Field(
        None,
        description="尺寸(cm)",
        example={"length": 20, "width": 15, "height": 10}
    )
    weight_kg: Optional[float] = Field(None, description="重量(kg)", example=0.3, gt=0)


class QuickScoreRequest(BaseModel):
    """快速评分请求"""
    product_name: str = Field(..., description="产品名称", example="Desk Organizer")


class BatchAnalysisRequest(BaseModel):
    """批量分析请求"""
    product_names: List[str] = Field(
        ...,
        description="产品名称列表",
        example=["Car Phone Holder", "Desk Organizer", "LED Strip Light"],
        max_items=20  # 限制最多20个
    )


class AnalysisResponse(BaseModel):
    """分析响应"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


# ==================== API Endpoints ====================

@router.post("/analyze", response_model=AnalysisResponse, summary="分析产品")
async def analyze_product(request: ProductAnalysisRequest):
    """
    完整产品分析

    **功能**:
    - 自动采集8大数据源
    - AI智能分析
    - 100分制评分
    - 生成爆款脚本
    - 推荐供应商
    - 利润测算

    **耗时**: 约5-10分钟（使用Mock数据时约5秒）

    **返回**:
    - 完整的分析报告
    - 评分详情
    - 决策建议
    """
    try:
        logger.info(f"📥 收到分析请求: {request.product_name}")

        # 调用分析服务
        result = await analysis_service.analyze_product(
            product_name=request.product_name,
            product_url=request.product_url,
            selling_price=request.selling_price,
            purchase_price_cny=request.purchase_price_cny,
            dimensions=request.dimensions,
            weight_kg=request.weight_kg
        )

        return AnalysisResponse(
            success=True,
            message=f"分析完成: {result['scoring']['total_score']}/100 ({result['scoring']['grade']}级)",
            data=result
        )

    except Exception as e:
        logger.error(f"❌ 分析失败: {e}")
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/quick-score", response_model=AnalysisResponse, summary="快速评分")
async def quick_score(request: QuickScoreRequest):
    """
    快速评分（仅返回评分，不返回详细分析）

    **功能**:
    - 快速评分
    - 核心指标
    - 简化建议

    **耗时**: 约1-2分钟（使用Mock数据时约2秒）

    **适用场景**:
    - 快速筛选大量产品
    - 初步判断产品潜力
    """
    try:
        logger.info(f"⚡ 收到快速评分请求: {request.product_name}")

        result = await analysis_service.quick_score(request.product_name)

        return AnalysisResponse(
            success=True,
            message=f"{result['total_score']}/100 ({result['grade']}级)",
            data=result
        )

    except Exception as e:
        logger.error(f"❌ 快速评分失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch-analyze", response_model=AnalysisResponse, summary="批量分析")
async def batch_analyze(request: BatchAnalysisRequest):
    """
    批量快速分析

    **功能**:
    - 批量快速评分（最多20个产品）
    - 自动排序（按分数从高到低）
    - 对比分析

    **耗时**: 约2-5分钟（取决于产品数量）

    **适用场景**:
    - 每日新品推荐
    - 产品对比
    - 快速筛选
    """
    try:
        logger.info(f"📦 收到批量分析请求: {len(request.product_names)} 个产品")

        if len(request.product_names) > 20:
            raise HTTPException(status_code=400, detail="批量分析最多支持20个产品")

        results = await analysis_service.batch_analyze(request.product_names)

        return AnalysisResponse(
            success=True,
            message=f"批量分析完成: {len(results)} 个产品",
            data={"products": results, "total": len(results)}
        )

    except Exception as e:
        logger.error(f"❌ 批量分析失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/demo", response_model=AnalysisResponse, summary="演示分析")
async def demo_analysis():
    """
    演示分析 - 使用预设产品

    **功能**:
    - 快速体验系统功能
    - 无需输入参数
    - 展示完整分析流程
    """
    try:
        logger.info("🎬 演示分析")

        result = await analysis_service.analyze_product(
            product_name="Car Phone Holder",
            selling_price=24.99,
            purchase_price_cny=18,
            dimensions={"length": 15, "width": 10, "height": 5},
            weight_kg=0.15
        )

        return AnalysisResponse(
            success=True,
            message="演示分析完成",
            data=result
        )

    except Exception as e:
        logger.error(f"❌ 演示分析失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health", summary="健康检查")
async def health_check():
    """产品分析服务健康检查"""
    return {
        "status": "healthy",
        "service": "product_analysis",
        "using_mock": analysis_service.config.should_use_mock(),
        "ai_enabled": not analysis_service.config.should_skip_ai()
    }
