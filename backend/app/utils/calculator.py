"""
计算工具
包括：利润计算、物流成本计算、评分计算等
"""

from typing import Dict, Any, Tuple
from app.core.config import settings


class ProfitCalculator:
    """利润计算器"""

    def __init__(self):
        self.cny_to_usd = settings.CNY_TO_USD_RATE
        self.platform_fee_rate = settings.DEFAULT_PLATFORM_FEE_RATE
        self.ad_cost_rate = settings.DEFAULT_AD_COST_RATE
        self.return_rate = settings.DEFAULT_RETURN_RATE
        self.packaging_cost = settings.DEFAULT_PACKAGING_COST

    def calculate_shipping_cost(
        self,
        length_cm: float,
        width_cm: float,
        height_cm: float,
        weight_kg: float
    ) -> Dict[str, Any]:
        """
        计算物流成本

        Args:
            length_cm: 长度(cm)
            width_cm: 宽度(cm)
            height_cm: 高度(cm)
            weight_kg: 重量(kg)

        Returns:
            物流成本详情
        """
        # 计算体积重
        volume_weight = (length_cm * width_cm * height_cm) / 6000

        # 计费重量 = max(体积重, 实际重)
        chargeable_weight = max(volume_weight, weight_kg)

        # 空运成本
        air_shipping_cost = chargeable_weight * settings.SHIPPING_COST_PER_KG

        # 仓储费（根据重量分级）
        if weight_kg < 0.5:
            warehouse_fee = settings.WAREHOUSE_FEE_SMALL
            tier = "small"
        elif weight_kg < 1.0:
            warehouse_fee = settings.WAREHOUSE_FEE_MEDIUM
            tier = "medium"
        else:
            warehouse_fee = settings.WAREHOUSE_FEE_LARGE
            tier = "large"

        # 总物流成本
        total_shipping_cost = air_shipping_cost + warehouse_fee

        return {
            "volume_weight_kg": round(volume_weight, 2),
            "actual_weight_kg": weight_kg,
            "chargeable_weight_kg": round(chargeable_weight, 2),
            "air_shipping_cost": round(air_shipping_cost, 2),
            "warehouse_fee": round(warehouse_fee, 2),
            "total_shipping_cost": round(total_shipping_cost, 2),
            "tier": tier
        }

    def calculate_profit(
        self,
        selling_price_usd: float,
        purchase_price_cny: float,
        length_cm: float,
        width_cm: float,
        height_cm: float,
        weight_kg: float,
        custom_platform_fee_rate: float = None,
        custom_ad_cost_rate: float = None
    ) -> Dict[str, Any]:
        """
        计算利润

        Args:
            selling_price_usd: 售价(USD)
            purchase_price_cny: 采购价(CNY)
            length_cm: 长度
            width_cm: 宽度
            height_cm: 高度
            weight_kg: 重量
            custom_platform_fee_rate: 自定义平台费率
            custom_ad_cost_rate: 自定义广告费率

        Returns:
            利润详情
        """
        # 采购成本(USD)
        purchase_cost_usd = purchase_price_cny * self.cny_to_usd

        # 物流成本
        shipping_details = self.calculate_shipping_cost(
            length_cm, width_cm, height_cm, weight_kg
        )
        shipping_cost = shipping_details["total_shipping_cost"]

        # 包装成本
        packaging_cost = self.packaging_cost

        # 平台费用
        platform_fee_rate = custom_platform_fee_rate or self.platform_fee_rate
        platform_fee = selling_price_usd * platform_fee_rate

        # 广告成本
        ad_cost_rate = custom_ad_cost_rate or self.ad_cost_rate
        ad_cost = selling_price_usd * ad_cost_rate

        # 退货预留
        return_reserve = selling_price_usd * self.return_rate

        # 总成本
        total_cost = (
            purchase_cost_usd +
            shipping_cost +
            packaging_cost +
            platform_fee +
            ad_cost +
            return_reserve
        )

        # 利润
        profit = selling_price_usd - total_cost

        # 利润率
        profit_margin = profit / selling_price_usd if selling_price_usd > 0 else 0

        # 各项成本占比
        cost_breakdown_percentage = {
            "purchase": round(purchase_cost_usd / selling_price_usd * 100, 1) if selling_price_usd > 0 else 0,
            "shipping": round(shipping_cost / selling_price_usd * 100, 1) if selling_price_usd > 0 else 0,
            "packaging": round(packaging_cost / selling_price_usd * 100, 1) if selling_price_usd > 0 else 0,
            "platform_fee": round(platform_fee / selling_price_usd * 100, 1) if selling_price_usd > 0 else 0,
            "ad_cost": round(ad_cost / selling_price_usd * 100, 1) if selling_price_usd > 0 else 0,
            "return_reserve": round(return_reserve / selling_price_usd * 100, 1) if selling_price_usd > 0 else 0,
            "profit": round(profit_margin * 100, 1),
        }

        return {
            "selling_price": round(selling_price_usd, 2),
            "costs": {
                "purchase_cost": round(purchase_cost_usd, 2),
                "shipping_cost": round(shipping_cost, 2),
                "packaging_cost": round(packaging_cost, 2),
                "platform_fee": round(platform_fee, 2),
                "ad_cost": round(ad_cost, 2),
                "return_reserve": round(return_reserve, 2),
                "total_cost": round(total_cost, 2),
            },
            "profit": round(profit, 2),
            "profit_margin": round(profit_margin, 4),
            "profit_margin_percentage": round(profit_margin * 100, 1),
            "cost_breakdown_percentage": cost_breakdown_percentage,
            "shipping_details": shipping_details,
            "is_profitable": profit > 0,
            "profit_level": self._get_profit_level(profit_margin),
        }

    def _get_profit_level(self, profit_margin: float) -> str:
        """根据利润率判断利润水平"""
        if profit_margin >= 0.5:
            return "excellent"  # 优秀 ≥50%
        elif profit_margin >= 0.35:
            return "good"  # 良好 35-50%
        elif profit_margin >= 0.25:
            return "acceptable"  # 可接受 25-35%
        elif profit_margin >= 0.15:
            return "low"  # 较低 15-25%
        elif profit_margin > 0:
            return "very_low"  # 很低 0-15%
        else:
            return "unprofitable"  # 不盈利

    def calculate_shipping_ratio(
        self,
        selling_price_usd: float,
        length_cm: float,
        width_cm: float,
        height_cm: float,
        weight_kg: float
    ) -> float:
        """计算物流成本占比"""
        shipping_details = self.calculate_shipping_cost(
            length_cm, width_cm, height_cm, weight_kg
        )
        shipping_cost = shipping_details["total_shipping_cost"]
        return shipping_cost / selling_price_usd if selling_price_usd > 0 else 0


class SizeScorer:
    """尺寸评分器"""

    def score_size_logistics(
        self,
        length_cm: float,
        width_cm: float,
        height_cm: float,
        weight_kg: float,
        selling_price_usd: float
    ) -> Tuple[float, Dict[str, Any]]:
        """
        尺寸与物流评分

        Returns:
            (评分, 详情)
        """
        calculator = ProfitCalculator()

        # 计算物流成本占比
        shipping_ratio = calculator.calculate_shipping_ratio(
            selling_price_usd, length_cm, width_cm, height_cm, weight_kg
        )

        # 根据占比评分
        if shipping_ratio < 0.15:
            score = 10.0  # 优秀
            level = "excellent"
        elif shipping_ratio < 0.25:
            score = 8.0  # 良好
            level = "good"
        elif shipping_ratio < 0.35:
            score = 6.0  # 一般
            level = "acceptable"
        elif shipping_ratio < 0.45:
            score = 4.0  # 较差
            level = "poor"
        else:
            score = 2.0  # 很差
            level = "very_poor"

        # 尺寸分级
        max_side = max(length_cm, width_cm, height_cm)
        if max_side < 30 and weight_kg < 0.5:
            size_tier = "small"
            tier_bonus = 0
        elif max_side < 50 and weight_kg < 1.0:
            size_tier = "medium"
            tier_bonus = 0
        elif max_side < 80 and weight_kg < 2.0:
            size_tier = "large"
            tier_bonus = -1
        else:
            size_tier = "extra_large"
            tier_bonus = -2

        final_score = max(0, min(10, score + tier_bonus))

        details = {
            "dimensions": {"length": length_cm, "width": width_cm, "height": height_cm},
            "weight_kg": weight_kg,
            "max_side_cm": max_side,
            "shipping_ratio": round(shipping_ratio, 4),
            "shipping_ratio_percentage": round(shipping_ratio * 100, 1),
            "size_tier": size_tier,
            "level": level,
            "recommendation": self._get_size_recommendation(size_tier, shipping_ratio)
        }

        return final_score, details

    def _get_size_recommendation(self, size_tier: str, shipping_ratio: float) -> str:
        """获取尺寸建议"""
        if size_tier == "small" and shipping_ratio < 0.15:
            return "完美尺寸，强烈推荐"
        elif size_tier == "medium" and shipping_ratio < 0.25:
            return "尺寸适中，可以考虑"
        elif size_tier == "large":
            return "尺寸较大，物流成本占比高，需优化"
        else:
            return "尺寸过大，不建议"


# 全局实例
profit_calculator = ProfitCalculator()
size_scorer = SizeScorer()
