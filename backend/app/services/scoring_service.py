"""
评分引擎 - 核心评分逻辑
实现9大维度的自动评分
"""

from typing import Dict, Any, Tuple
from app.core.config import settings
from app.utils.calculator import profit_calculator, size_scorer
from loguru import logger


class ScoringService:
    """评分服务 - 100分制评分系统"""

    def __init__(self):
        self.weights = {
            "market_demand": settings.WEIGHT_MARKET_DEMAND,
            "functional_value": settings.WEIGHT_FUNCTIONAL_VALUE,
            "emotional_value": settings.WEIGHT_EMOTIONAL_VALUE,
            "content_value": settings.WEIGHT_CONTENT_VALUE,
            "pleasure_pain": settings.WEIGHT_PLEASURE_PAIN,
            "us_market_fit": settings.WEIGHT_US_MARKET_FIT,
            "size_logistics": settings.WEIGHT_SIZE_LOGISTICS,
            "competition": settings.WEIGHT_COMPETITION,
            "supply_pricing": settings.WEIGHT_SUPPLY_PRICING,
        }

    def score_market_demand(self, data_sources: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        """
        1. 市场需求评分 (10分)

        基于：
        - Google Trends热度
        - 数据源验证数量
        - 趋势方向
        """
        score = 0.0
        details = {}

        google_trends = data_sources.get("google_trends", {})
        tiktok = data_sources.get("tiktok", {})
        alibaba = data_sources.get("alibaba", {})

        # Google Trends热度评分 (0-5分)
        trends_score = google_trends.get("score", 0)
        if trends_score >= 70:
            score += 5.0
        elif trends_score >= 50:
            score += 4.0
        elif trends_score >= 30:
            score += 2.5
        else:
            score += 1.0

        # 趋势方向评分 (0-2分)
        trend_direction = google_trends.get("trend", "").lower()
        if trend_direction == "rising":
            score += 2.0
        elif trend_direction == "stable":
            score += 1.5
        else:
            score += 0.5

        # 数据源验证评分 (0-3分)
        verified_sources = 0
        if google_trends.get("score", 0) > 0:
            verified_sources += 1
        if tiktok.get("video_count", 0) > 100:
            verified_sources += 1
        if alibaba.get("sales_growth", 0) > 20:
            verified_sources += 1

        if verified_sources >= 3:
            score += 3.0
        elif verified_sources == 2:
            score += 2.0
        else:
            score += 1.0

        details = {
            "google_trends_score": trends_score,
            "trend_direction": trend_direction,
            "verified_sources": verified_sources,
            "evaluation": "强" if score >= 8 else "中" if score >= 5 else "弱"
        }

        return min(10.0, score), details

    def score_content_value(self, data_sources: Dict[str, Any], ai_analysis: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        """
        4. 内容价值评分 (15分) - 最关键

        基于：
        - 视觉冲击力 (AI分析)
        - TikTok视频表现
        - 可拍脚本数量
        """
        score = 0.0
        details = {}

        tiktok = data_sources.get("tiktok", {})
        vision_analysis = ai_analysis.get("vision", {})

        # 前3秒吸引力 (0-5分) - 基于视觉冲击力
        visual_impact = vision_analysis.get("visual_impact", 5)
        hook_score = (visual_impact / 10) * 5
        score += hook_score

        # 视觉表现力 (0-4分)
        aesthetics = vision_analysis.get("aesthetics_score", 5)
        quality = vision_analysis.get("quality_feel", 5)
        visual_score = ((aesthetics + quality) / 20) * 4
        score += visual_score

        # 可拍脚本数量 (0-3分)
        # 基于TikTok视频数量和多样性
        video_count = tiktok.get("video_count", 0)
        if video_count >= 500:
            script_score = 3.0  # 10+脚本
        elif video_count >= 200:
            script_score = 2.5  # 5-10脚本
        elif video_count >= 100:
            script_score = 2.0  # 3-5脚本
        else:
            script_score = 1.0  # <3脚本
        score += script_score

        # 混剪友好度 (0-2分)
        # 基于视频数量
        if video_count >= 300:
            remix_score = 2.0
        elif video_count >= 100:
            remix_score = 1.5
        else:
            remix_score = 1.0
        score += remix_score

        # AI可生成性 (0-1分)
        filming_difficulty = vision_analysis.get("filming_difficulty", "medium")
        if filming_difficulty == "easy":
            ai_score = 1.0
        elif filming_difficulty == "medium":
            ai_score = 0.6
        else:
            ai_score = 0.3
        score += ai_score

        details = {
            "hook_strength": round(hook_score, 1),
            "visual_impact": round(visual_score, 1),
            "script_potential": round(script_score, 1),
            "remix_friendly": round(remix_score, 1),
            "ai_generable": round(ai_score, 1),
            "filming_difficulty": filming_difficulty,
            "evaluation": "优秀" if score >= 12 else "良好" if score >= 9 else "一般"
        }

        return min(15.0, score), details

    def score_competition(self, data_sources: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        """
        8. 竞争强度评分 (10分)

        基于：
        - TikTok视频数量
        - TikTok商品数量
        - 价格竞争情况
        """
        score = 10.0  # 默认满分，有竞争问题则扣分
        details = {}

        tiktok = data_sources.get("tiktok", {})
        alibaba = data_sources.get("alibaba", {})

        video_count = tiktok.get("video_count", 0)
        shop_count = tiktok.get("shop_count", 0)

        # 判断竞争等级
        if video_count < 100:
            competition_level = "level_1"  # 蓝海
            level_score = 8.0
            recommendation = "需求未验证，高风险"
        elif 100 <= video_count < 500:
            competition_level = "level_2"  # 黄金期
            level_score = 10.0
            recommendation = "黄金窗口期，强烈推荐"
        elif 500 <= video_count < 2000:
            competition_level = "level_3"  # 增长期
            level_score = 7.0
            recommendation = "需要差异化"
        elif 2000 <= video_count < 5000:
            competition_level = "level_4"  # 红海
            level_score = 4.0
            recommendation = "竞争激烈，谨慎"
        else:
            competition_level = "level_5"  # 饱和
            level_score = 2.0
            recommendation = "不建议进入"

        score = level_score

        # 根据商品数量调整
        if shop_count > 500:
            score -= 1.0
        elif shop_count > 200:
            score -= 0.5

        # 价格战判断
        alibaba_suppliers = alibaba.get("suppliers_count", 0)
        if alibaba_suppliers > 200:
            score -= 0.5
            price_war = True
        else:
            price_war = False

        details = {
            "competition_level": competition_level,
            "video_count": video_count,
            "shop_count": shop_count,
            "price_war": price_war,
            "recommendation": recommendation,
            "evaluation": self._get_competition_evaluation(competition_level)
        }

        return max(0, min(10.0, score)), details

    def score_supply_pricing(
        self,
        data_sources: Dict[str, Any],
        selling_price: float,
        purchase_price_cny: float,
        dimensions: Dict[str, float],
        weight_kg: float
    ) -> Tuple[float, Dict[str, Any]]:
        """
        9. 供应链与定价评分 (15分) - 关键

        基于：
        - 采购成本
        - 售价区间
        - 供应链成熟度
        """
        score = 0.0
        details = {}

        alibaba = data_sources.get("alibaba", {})

        # 利润计算
        profit_result = profit_calculator.calculate_profit(
            selling_price_usd=selling_price,
            purchase_price_cny=purchase_price_cny,
            length_cm=dimensions.get("length", 20),
            width_cm=dimensions.get("width", 15),
            height_cm=dimensions.get("height", 10),
            weight_kg=weight_kg
        )

        # 利润率评分 (0-5分)
        profit_margin = profit_result["profit_margin"]
        if profit_margin >= 0.6:
            profit_score = 5.0
        elif profit_margin >= 0.5:
            profit_score = 4.5
        elif profit_margin >= 0.4:
            profit_score = 4.0
        elif profit_margin >= 0.3:
            profit_score = 3.5
        elif profit_margin >= 0.2:
            profit_score = 2.5
        else:
            profit_score = 1.0
        score += profit_score

        # 售价区间评分 (0-5分)
        if 14.99 <= selling_price <= 29.99:
            price_score = 5.0  # 完美价格带
        elif 9.99 <= selling_price < 14.99 or 29.99 < selling_price <= 39.99:
            price_score = 4.0  # 较好价格带
        elif 39.99 < selling_price <= 49.99:
            price_score = 3.0  # 一般价格带
        elif 49.99 < selling_price <= 79.99:
            price_score = 2.0  # 较高价格带
        else:
            price_score = 1.0  # 高价格带
        score += price_score

        # 供应链成熟度评分 (0-5分)
        suppliers_count = alibaba.get("suppliers_count", 0)
        has_crossborder = alibaba.get("has_crossborder", False)
        supports_dropship = alibaba.get("supports_dropship", False)

        supply_score = 0
        if suppliers_count >= 50:
            supply_score += 2.0
        elif suppliers_count >= 20:
            supply_score += 1.5
        else:
            supply_score += 0.5

        if has_crossborder:
            supply_score += 1.5
        if supports_dropship:
            supply_score += 1.0
        if alibaba.get("moq", 100) <= 50:
            supply_score += 0.5

        score += supply_score

        details = {
            "profit_margin": round(profit_margin, 4),
            "profit_margin_percentage": round(profit_margin * 100, 1),
            "profit_level": profit_result["profit_level"],
            "selling_price": selling_price,
            "price_tier": self._get_price_tier(selling_price),
            "suppliers_count": suppliers_count,
            "supply_chain_maturity": "成熟" if supply_score >= 4 else "一般" if supply_score >= 2 else "不成熟",
            "profit_breakdown": profit_result["costs"]
        }

        return min(15.0, score), details

    def calculate_total_score(
        self,
        data_sources: Dict[str, Any],
        ai_analysis: Dict[str, Any],
        product_params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        计算总分

        Args:
            data_sources: 数据源数据
            ai_analysis: AI分析结果
            product_params: 产品参数（售价、尺寸等）

        Returns:
            完整的评分结果
        """
        logger.info("🎯 开始计算总分...")

        scores = {}

        # 1. 市场需求 (10分)
        market_score, market_detail = self.score_market_demand(data_sources)
        scores["market_demand"] = {"score": market_score, "detail": market_detail}

        # 2. 功能价值 (10分) - 简化评分，基于AI分析
        functional_score = 7.0  # 默认分数，实际应该用AI深度分析
        scores["functional_value"] = {"score": functional_score, "detail": {}}

        # 3. 情绪价值 (10分) - 基于用户情绪分析
        text_analysis = ai_analysis.get("text", {})
        sentiment = text_analysis.get("user_sentiment", 0.7)
        emotional_score = sentiment * 10
        scores["emotional_value"] = {"score": emotional_score, "detail": {"sentiment": sentiment}}

        # 4. 内容价值 (15分) - 最关键
        content_score, content_detail = self.score_content_value(data_sources, ai_analysis)
        scores["content_value"] = {"score": content_score, "detail": content_detail}

        # 5. 爽点/痛点强度 (10分) - 简化评分
        pleasure_score = 7.0  # 默认分数
        scores["pleasure_pain"] = {"score": pleasure_score, "detail": {}}

        # 6. 美国市场适配 (10分) - 简化评分
        us_fit_score = 8.0  # 默认分数，实际应该检查30项Checklist
        scores["us_market_fit"] = {"score": us_fit_score, "detail": {}}

        # 7. 尺寸与物流 (10分)
        dimensions = product_params.get("dimensions", {"length": 20, "width": 15, "height": 10})
        weight = product_params.get("weight_kg", 0.3)
        selling_price = product_params.get("selling_price", 24.99)

        size_score, size_detail = size_scorer.score_size_logistics(
            length_cm=dimensions.get("length", 20),
            width_cm=dimensions.get("width", 15),
            height_cm=dimensions.get("height", 10),
            weight_kg=weight,
            selling_price_usd=selling_price
        )
        scores["size_logistics"] = {"score": size_score, "detail": size_detail}

        # 8. 竞争强度 (10分)
        competition_score, competition_detail = self.score_competition(data_sources)
        scores["competition"] = {"score": competition_score, "detail": competition_detail}

        # 9. 供应链与定价 (15分) - 关键
        purchase_price = product_params.get("purchase_price_cny", 20)
        supply_score, supply_detail = self.score_supply_pricing(
            data_sources, selling_price, purchase_price, dimensions, weight
        )
        scores["supply_pricing"] = {"score": supply_score, "detail": supply_detail}

        # 计算总分
        total_score = sum(s["score"] for s in scores.values())

        # 计算等级
        grade = settings.calculate_grade(total_score)

        # 获取推荐
        recommendation = settings.get_recommendation_by_score(total_score)

        result = {
            "total_score": round(total_score, 2),
            "grade": grade,
            "scores": scores,
            "recommendation": recommendation,
            "calculated_at": "now"
        }

        logger.info(f"✅ 评分完成: {total_score}/100 ({grade}级)")

        return result

    def _get_competition_evaluation(self, level: str) -> str:
        """获取竞争评价"""
        evaluations = {
            "level_1": "蓝海",
            "level_2": "黄金期",
            "level_3": "增长期",
            "level_4": "红海",
            "level_5": "饱和"
        }
        return evaluations.get(level, "未知")

    def _get_price_tier(self, price: float) -> str:
        """获取价格分级"""
        if 14.99 <= price <= 29.99:
            return "perfect"
        elif 9.99 <= price <= 39.99:
            return "good"
        elif 39.99 < price <= 49.99:
            return "medium"
        elif 49.99 < price <= 79.99:
            return "high"
        else:
            return "very_high"


# 全局评分服务实例
scoring_service = ScoringService()
