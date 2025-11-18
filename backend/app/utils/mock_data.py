"""
Mock数据生成器
用于在开发阶段或无API Key时提供模拟数据
"""

import random
from typing import Dict, Any, List
from datetime import datetime, timedelta


class MockDataGenerator:
    """Mock数据生成器"""

    def __init__(self):
        self.product_names = [
            "Car Phone Holder",
            "Desk Organizer",
            "Cleaning Brush",
            "LED Strip Light",
            "Pet Grooming Tool",
            "Kitchen Gadget Set",
            "Portable Charger",
            "Cable Organizer",
            "Shower Head Filter",
            "Magnetic Hooks"
        ]

    def generate_alibaba_data(self, product_name: str) -> Dict[str, Any]:
        """生成1688数据"""
        return {
            "sales_7d": random.randint(500, 5000),
            "sales_growth": round(random.uniform(10, 150), 1),
            "suppliers_count": random.randint(30, 200),
            "avg_price": round(random.uniform(10, 50), 2),
            "price_range": [
                round(random.uniform(8, 15), 2),
                round(random.uniform(30, 60), 2)
            ],
            "moq": random.choice([10, 20, 30, 50, 100]),
            "has_crossborder": True,
            "supports_dropship": random.choice([True, False]),
        }

    def generate_tiktok_data(self, product_name: str) -> Dict[str, Any]:
        """生成TikTok数据"""
        video_count = random.randint(100, 3000)
        return {
            "video_count": video_count,
            "video_count_last_30d": int(video_count * random.uniform(0.2, 0.4)),
            "avg_views": random.randint(100000, 5000000),
            "top_video_views": random.randint(1000000, 10000000),
            "shop_count": random.randint(10, 500),
            "avg_price": round(random.uniform(14.99, 49.99), 2),
            "price_range": [14.99, 49.99],
            "avg_rating": round(random.uniform(4.0, 4.9), 1),
        }

    def generate_google_trends_data(self, product_name: str) -> Dict[str, Any]:
        """生成Google Trends数据"""
        score = random.randint(30, 90)
        return {
            "score": score,
            "trend": random.choice(["rising", "stable", "falling"]),
            "region_interest": {
                "California": random.randint(80, 100),
                "Texas": random.randint(70, 95),
                "Florida": random.randint(60, 90),
                "New York": random.randint(65, 85),
            },
            "related_queries": [
                f"{product_name} amazon",
                f"best {product_name}",
                f"{product_name} review",
                f"cheap {product_name}",
            ]
        }

    def generate_amazon_data(self, product_name: str) -> Dict[str, Any]:
        """生成Amazon数据"""
        return {
            "rank": random.randint(100, 10000),
            "rank_change": random.randint(-200, 200),
            "avg_price": round(random.uniform(19.99, 59.99), 2),
            "rating": round(random.uniform(3.5, 4.8), 1),
            "review_count": random.randint(100, 5000),
            "bsr_category": "Home & Kitchen",
        }

    def generate_ai_vision_analysis(self, product_name: str) -> Dict[str, Any]:
        """生成AI视觉分析（模拟GPT-4 Vision）"""
        return {
            "aesthetics_score": random.randint(6, 10),
            "quality_feel": random.randint(6, 10),
            "visual_impact": random.randint(5, 10),
            "filming_difficulty": random.choice(["easy", "medium", "hard"]),
            "color_appeal": random.choice(["high", "medium", "low"]),
            "professional_look": random.choice([True, False]),
            "analysis": f"这款{product_name}具有良好的视觉吸引力，产品设计简洁现代，适合拍摄展示。"
        }

    def generate_ai_text_analysis(self, product_name: str) -> Dict[str, Any]:
        """生成AI文本分析（模拟GPT-4）"""
        pain_points = [
            "使用不便",
            "价格过高",
            "质量问题",
            "尺寸不合适",
            "功能单一"
        ]

        return {
            "pain_points": random.sample(pain_points, 2),
            "user_sentiment": round(random.uniform(0.6, 0.95), 2),
            "key_features": [
                "便携设计",
                "易于安装",
                "多功能",
                "高品质材料"
            ][:random.randint(2, 4)],
            "target_audience": random.choice([
                "年轻上班族",
                "家庭主妇",
                "学生群体",
                "车主"
            ]),
            "purchase_motivation": random.choice([
                "解决痛点",
                "提升生活品质",
                "价格优惠",
                "跟风购买"
            ])
        }

    def generate_scripts(self, product_name: str) -> List[Dict[str, Any]]:
        """生成脚本库（模拟）"""
        script_types = [
            {
                "type": "pain_solution",
                "title": "痛点+解决方案",
                "description": "展示用户痛点，然后展示产品如何解决",
                "difficulty": "easy",
                "expected_effect": "strong",
            },
            {
                "type": "before_after",
                "title": "使用前后对比",
                "description": "强烈的视觉对比，展示使用前后的差异",
                "difficulty": "easy",
                "expected_effect": "extreme",
            },
            {
                "type": "demo",
                "title": "产品演示",
                "description": "详细展示产品使用方法和效果",
                "difficulty": "medium",
                "expected_effect": "strong",
            },
            {
                "type": "unboxing",
                "title": "开箱体验",
                "description": "展示开箱过程，突出产品质感",
                "difficulty": "easy",
                "expected_effect": "medium",
            },
            {
                "type": "scenario",
                "title": "使用场景展示",
                "description": "在真实场景中展示产品价值",
                "difficulty": "medium",
                "expected_effect": "strong",
            }
        ]

        scripts = []
        for i, script_type in enumerate(random.sample(script_types, min(3, len(script_types))), 1):
            scripts.append({
                "rank": i,
                "script_type": script_type["type"],
                "title": f"脚本 #{i}: {script_type['title']}",
                "description": script_type["description"],
                "script_content": {
                    "hook": f"前3秒展示{product_name}的惊艳效果",
                    "body": "详细展示产品功能和使用方法",
                    "cta": "立即购买/点击链接",
                    "duration": "15-30秒"
                },
                "reference_videos": [
                    {
                        "url": f"https://tiktok.com/@user{i}/video/123456789",
                        "views": random.randint(500000, 5000000),
                        "likes": random.randint(50000, 500000),
                    }
                ],
                "difficulty": script_type["difficulty"],
                "expected_effect": script_type["expected_effect"],
            })

        return scripts

    def generate_suppliers(self, product_name: str) -> List[Dict[str, Any]]:
        """生成供应商推荐"""
        suppliers = []
        for i in range(1, 6):  # TOP 5
            suppliers.append({
                "rank": i,
                "supplier_name": f"优质供应商 #{i}",
                "price": round(random.uniform(10, 40), 2),
                "moq": random.choice([10, 20, 30, 50]),
                "rating": round(random.uniform(4.0, 4.9), 1),
                "review_count": random.randint(100, 1000),
                "one_piece_dropship": random.choice([True, False]),
                "us_warehouse": random.choice([True, False]),
                "lead_time": random.randint(3, 15),
                "advantages": random.sample([
                    "支持一件代发",
                    "美国仓直发",
                    "质量稳定",
                    "快速发货",
                    "价格优惠",
                    "售后完善"
                ], 3)
            })

        return suppliers

    def generate_full_analysis(self, product_name: str) -> Dict[str, Any]:
        """生成完整的产品分析数据"""
        return {
            "product_name": product_name,
            "data_sources": {
                "alibaba": self.generate_alibaba_data(product_name),
                "tiktok": self.generate_tiktok_data(product_name),
                "google_trends": self.generate_google_trends_data(product_name),
                "amazon": self.generate_amazon_data(product_name),
            },
            "ai_analysis": {
                "vision": self.generate_ai_vision_analysis(product_name),
                "text": self.generate_ai_text_analysis(product_name),
            },
            "scripts": self.generate_scripts(product_name),
            "suppliers": self.generate_suppliers(product_name),
            "generated_at": datetime.now().isoformat(),
            "is_mock": True,  # 标记为模拟数据
        }


# 全局Mock数据生成器实例
mock_generator = MockDataGenerator()


# 便捷函数
def get_mock_analysis(product_name: str) -> Dict[str, Any]:
    """获取Mock分析数据"""
    return mock_generator.generate_full_analysis(product_name)
