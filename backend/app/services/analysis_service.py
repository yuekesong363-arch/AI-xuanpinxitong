"""
产品分析服务 - 核心业务逻辑
整合数据采集、AI分析、评分等所有模块
"""

from typing import Dict, Any, Optional
from loguru import logger

from app.services.config_service import config_service
from app.services.scoring_service import scoring_service
from app.utils.mock_data import mock_generator
from app.utils.calculator import profit_calculator


class ProductAnalysisService:
    """产品分析服务 - 整合所有分析功能"""

    def __init__(self):
        self.config = config_service
        self.scorer = scoring_service
        self.mock = mock_generator

    async def analyze_product(
        self,
        product_name: str,
        product_url: Optional[str] = None,
        selling_price: Optional[float] = None,
        purchase_price_cny: Optional[float] = None,
        dimensions: Optional[Dict[str, float]] = None,
        weight_kg: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        分析产品 - 主入口

        Args:
            product_name: 产品名称（英文）
            product_url: 产品链接（1688等）
            selling_price: 预期售价(USD)
            purchase_price_cny: 采购价(CNY)
            dimensions: 尺寸 {"length": 20, "width": 15, "height": 10}
            weight_kg: 重量(kg)

        Returns:
            完整的分析结果
        """
        logger.info(f"🔍 开始分析产品: {product_name}")

        # 检查配置
        using_mock = self.config.should_use_mock()
        if using_mock:
            logger.info("⚠️  使用Mock数据（未配置API Key或开启Mock模式）")

        # 第1步：数据采集
        logger.info("📊 步骤1/4: 数据采集...")
        data_sources = await self._collect_data(product_name, product_url)

        # 第2步：AI分析
        logger.info("🤖 步骤2/4: AI分析...")
        ai_analysis = await self._ai_analysis(product_name, data_sources)

        # 第3步：脚本和供应商生成
        logger.info("📝 步骤3/4: 生成脚本和供应商推荐...")
        scripts = await self._generate_scripts(product_name, data_sources)
        suppliers = await self._generate_suppliers(product_name, data_sources)

        # 第4步：评分
        logger.info("🎯 步骤4/4: 评分...")

        # 准备产品参数（使用默认值如果没有提供）
        product_params = {
            "selling_price": selling_price or self._estimate_selling_price(data_sources),
            "purchase_price_cny": purchase_price_cny or self._estimate_purchase_price(data_sources),
            "dimensions": dimensions or {"length": 20, "width": 15, "height": 10},
            "weight_kg": weight_kg or 0.3,
        }

        # 计算评分
        scoring_result = self.scorer.calculate_total_score(
            data_sources=data_sources,
            ai_analysis=ai_analysis,
            product_params=product_params
        )

        # 计算详细利润
        profit_detail = profit_calculator.calculate_profit(
            selling_price_usd=product_params["selling_price"],
            purchase_price_cny=product_params["purchase_price_cny"],
            length_cm=product_params["dimensions"]["length"],
            width_cm=product_params["dimensions"]["width"],
            height_cm=product_params["dimensions"]["height"],
            weight_kg=product_params["weight_kg"]
        )

        # 组装完整结果
        result = {
            "product_name": product_name,
            "product_url": product_url,
            "analysis_id": self._generate_analysis_id(),

            # 数据源
            "data_sources": data_sources,

            # AI分析
            "ai_analysis": ai_analysis,

            # 评分结果
            "scoring": scoring_result,

            # 利润详情
            "profit_detail": profit_detail,

            # 脚本库
            "scripts": scripts,

            # 供应商推荐
            "suppliers": suppliers,

            # 产品参数
            "product_params": product_params,

            # 元数据
            "metadata": {
                "using_mock_data": using_mock,
                "analyzed_at": self._get_timestamp(),
                "analysis_version": "1.0.0"
            }
        }

        logger.info(f"✅ 分析完成: {product_name} - {scoring_result['total_score']}/100 ({scoring_result['grade']}级)")

        return result

    async def _collect_data(self, product_name: str, product_url: Optional[str]) -> Dict[str, Any]:
        """数据采集"""
        if self.config.should_skip_scraping() or self.config.should_use_mock():
            # 使用Mock数据
            logger.info("   使用Mock数据源...")
            return {
                "alibaba": self.mock.generate_alibaba_data(product_name),
                "tiktok": self.mock.generate_tiktok_data(product_name),
                "google_trends": self.mock.generate_google_trends_data(product_name),
                "amazon": self.mock.generate_amazon_data(product_name),
            }
        else:
            # TODO: 实际爬虫采集
            logger.info("   调用真实爬虫...")
            # 这里将来实现真实爬虫
            return {}

    async def _ai_analysis(self, product_name: str, data_sources: Dict[str, Any]) -> Dict[str, Any]:
        """AI分析"""
        if self.config.should_skip_ai() or self.config.should_use_mock():
            # 使用Mock AI分析
            logger.info("   使用Mock AI分析...")
            return {
                "vision": self.mock.generate_ai_vision_analysis(product_name),
                "text": self.mock.generate_ai_text_analysis(product_name),
            }
        else:
            # TODO: 调用真实AI API
            logger.info("   调用OpenAI API...")
            # 这里将来实现真实AI调用
            return {}

    async def _generate_scripts(self, product_name: str, data_sources: Dict[str, Any]) -> list:
        """生成脚本库"""
        logger.info("   生成脚本库...")
        return self.mock.generate_scripts(product_name)

    async def _generate_suppliers(self, product_name: str, data_sources: Dict[str, Any]) -> list:
        """生成供应商推荐"""
        logger.info("   生成供应商推荐...")
        return self.mock.generate_suppliers(product_name)

    def _estimate_selling_price(self, data_sources: Dict[str, Any]) -> float:
        """估算售价（基于市场数据）"""
        tiktok_price = data_sources.get("tiktok", {}).get("avg_price", 24.99)
        amazon_price = data_sources.get("amazon", {}).get("avg_price", 24.99)
        return round((tiktok_price + amazon_price) / 2, 2)

    def _estimate_purchase_price(self, data_sources: Dict[str, Any]) -> float:
        """估算采购价（基于1688数据）"""
        alibaba_price = data_sources.get("alibaba", {}).get("avg_price", 20)
        return alibaba_price

    def _generate_analysis_id(self) -> str:
        """生成分析ID"""
        import uuid
        return str(uuid.uuid4())[:8]

    def _get_timestamp(self) -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()

    async def quick_score(self, product_name: str) -> Dict[str, Any]:
        """快速评分（仅返回评分，不返回详细分析）"""
        logger.info(f"⚡ 快速评分: {product_name}")

        data_sources = await self._collect_data(product_name, None)
        ai_analysis = await self._ai_analysis(product_name, data_sources)

        product_params = {
            "selling_price": self._estimate_selling_price(data_sources),
            "purchase_price_cny": self._estimate_purchase_price(data_sources),
            "dimensions": {"length": 20, "width": 15, "height": 10},
            "weight_kg": 0.3,
        }

        scoring_result = self.scorer.calculate_total_score(
            data_sources=data_sources,
            ai_analysis=ai_analysis,
            product_params=product_params
        )

        return {
            "product_name": product_name,
            "total_score": scoring_result["total_score"],
            "grade": scoring_result["grade"],
            "recommendation": scoring_result["recommendation"],
            "key_metrics": {
                "market_demand": scoring_result["scores"]["market_demand"]["score"],
                "content_value": scoring_result["scores"]["content_value"]["score"],
                "competition": scoring_result["scores"]["competition"]["score"],
                "profit_margin": scoring_result["scores"]["supply_pricing"]["detail"].get("profit_margin_percentage", 0),
            }
        }

    async def batch_analyze(self, product_names: list[str]) -> list[Dict[str, Any]]:
        """批量分析（快速评分）"""
        logger.info(f"📦 批量分析 {len(product_names)} 个产品...")

        results = []
        for product_name in product_names:
            try:
                result = await self.quick_score(product_name)
                results.append(result)
            except Exception as e:
                logger.error(f"❌ 分析失败: {product_name} - {e}")
                results.append({
                    "product_name": product_name,
                    "error": str(e),
                    "total_score": 0,
                    "grade": "F"
                })

        # 按分数排序
        results.sort(key=lambda x: x.get("total_score", 0), reverse=True)

        logger.info(f"✅ 批量分析完成: {len(results)} 个产品")
        return results


# 全局分析服务实例
analysis_service = ProductAnalysisService()
