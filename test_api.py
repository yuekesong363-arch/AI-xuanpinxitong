#!/usr/bin/env python3
"""
AI选品系统 - 快速测试脚本
"""

import requests
import json

# API基础URL
BASE_URL = "http://localhost:8000"

def print_json(data):
    """美化打印JSON"""
    print(json.dumps(data, indent=2, ensure_ascii=False))

def test_config_status():
    """测试1: 配置状态"""
    print("\n" + "="*60)
    print("测试1: 查看配置状态")
    print("="*60)

    response = requests.get(f"{BASE_URL}/api/v1/config/status")
    print_json(response.json())

def test_demo_analysis():
    """测试2: 演示分析"""
    print("\n" + "="*60)
    print("测试2: 演示产品分析")
    print("="*60)

    response = requests.get(f"{BASE_URL}/api/v1/products/demo")
    result = response.json()

    if result["success"]:
        data = result["data"]
        scoring = data["scoring"]

        print(f"\n产品名称: {data['product_name']}")
        print(f"总分: {scoring['total_score']}/100")
        print(f"等级: {scoring['grade']}")
        print(f"建议: {scoring['recommendation']['message']}")

        print("\n各维度得分:")
        for key, value in scoring['scores'].items():
            print(f"  - {key}: {value['score']}")

def test_quick_score():
    """测试3: 快速评分"""
    print("\n" + "="*60)
    print("测试3: 快速评分")
    print("="*60)

    products = ["Desk Organizer", "LED Strip Light", "Pet Grooming Tool"]

    for product in products:
        response = requests.post(
            f"{BASE_URL}/api/v1/products/quick-score",
            json={"product_name": product}
        )
        result = response.json()

        if result["success"]:
            data = result["data"]
            print(f"\n{product}:")
            print(f"  总分: {data['total_score']}/100")
            print(f"  等级: {data['grade']}")
            print(f"  建议: {data['recommendation']['message']}")

def test_batch_analysis():
    """测试4: 批量分析"""
    print("\n" + "="*60)
    print("测试4: 批量分析")
    print("="*60)

    response = requests.post(
        f"{BASE_URL}/api/v1/products/batch-analyze",
        json={
            "product_names": [
                "Car Phone Holder",
                "Desk Organizer",
                "LED Strip Light",
                "Cleaning Brush",
                "Kitchen Gadget Set"
            ]
        }
    )
    result = response.json()

    if result["success"]:
        products = result["data"]["products"]
        print(f"\n分析了 {len(products)} 个产品，按分数排序:\n")

        for i, p in enumerate(products, 1):
            print(f"{i}. {p['product_name']}: {p['total_score']}/100 ({p['grade']}级)")

def main():
    """主函数"""
    print("\n🎉 AI选品系统 - 功能测试")
    print("="*60)

    try:
        # 测试服务连接
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ 服务连接成功!")
        else:
            print("❌ 服务连接失败!")
            return

        # 运行测试
        test_config_status()
        test_demo_analysis()
        test_quick_score()
        test_batch_analysis()

        print("\n" + "="*60)
        print("✅ 所有测试完成!")
        print("="*60)

        print("\n💡 提示:")
        print("- 访问 http://localhost:8000/docs 查看完整API文档")
        print("- 查看 docs/QUICK_START.md 了解更多用法")

    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务，请确保后端服务正在运行")
        print("   启动命令: cd backend && python -m uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    main()
