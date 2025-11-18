# 快速开始 - AI选品系统

> 5分钟上手指南

---

## 🚀 快速启动

### 方式1：Docker一键启动（推荐）

```bash
# 1. 克隆项目（如果还没有）
git clone <your-repo-url>
cd AI-xuanpinxitong

# 2. 启动所有服务
docker-compose up -d

# 3. 查看日志
docker-compose logs -f backend

# 4. 访问API文档
open http://localhost:8000/docs
```

### 方式2：本地开发

```bash
# 1. 安装依赖
cd backend
pip install -r requirements.txt

# 2. 启动服务
uvicorn main:app --reload

# 3. 访问
open http://localhost:8000/docs
```

---

## 📝 第一次使用

### 步骤1：查看配置状态

```bash
curl http://localhost:8000/api/v1/config/status
```

**响应示例**：
```json
{
  "success": true,
  "message": "获取状态成功",
  "data": {
    "openai_configured": false,
    "can_use_ai": false,
    "can_scrape": false,
    "using_mock": true
  }
}
```

**说明**：
- `using_mock: true` 表示当前使用Mock数据
- 您可以直接使用系统，无需配置API Key
- 所有功能正常运行，只是使用模拟数据

---

### 步骤2：试用演示分析

```bash
curl http://localhost:8000/api/v1/products/demo
```

**功能**：
- 自动分析预设产品"Car Phone Holder"
- 返回完整的分析报告
- 包括评分、脚本、供应商等

**预计耗时**：约2-5秒（使用Mock数据）

---

### 步骤3：分析自己的产品

```bash
curl -X POST http://localhost:8000/api/v1/products/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Desk Organizer",
    "selling_price": 29.99,
    "purchase_price_cny": 25,
    "dimensions": {"length": 30, "width": 20, "height": 15},
    "weight_kg": 0.5
  }'
```

**参数说明**：
- `product_name`: 产品名称（必填）
- `selling_price`: 预期售价USD（可选，系统会自动估算）
- `purchase_price_cny`: 采购价CNY（可选）
- `dimensions`: 尺寸cm（可选）
- `weight_kg`: 重量kg（可选）

---

## 🎯 核心功能

### 1. 完整产品分析

**API**: `POST /api/v1/products/analyze`

**功能**：
- ✅ 9大维度自动评分
- ✅ 100分制总分
- ✅ S/A/B/C/D等级判定
- ✅ 15+爆款脚本
- ✅ TOP 5供应商推荐
- ✅ 详细利润测算
- ✅ 决策建议

**示例**：
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/products/analyze",
    json={
        "product_name": "LED Strip Light",
        "selling_price": 24.99
    }
)

result = response.json()
print(f"总分: {result['data']['scoring']['total_score']}/100")
print(f"等级: {result['data']['scoring']['grade']}")
print(f"建议: {result['data']['scoring']['recommendation']['message']}")
```

---

### 2. 快速评分

**API**: `POST /api/v1/products/quick-score`

**功能**：
- ⚡ 快速评分（仅返回核心指标）
- 适合大量产品的初步筛选

**示例**：
```bash
curl -X POST http://localhost:8000/api/v1/products/quick-score \
  -H "Content-Type: application/json" \
  -d '{"product_name": "Car Phone Holder"}'
```

---

### 3. 批量分析

**API**: `POST /api/v1/products/batch-analyze`

**功能**：
- 📦 一次分析最多20个产品
- 自动排序（按分数从高到低）

**示例**：
```python
response = requests.post(
    "http://localhost:8000/api/v1/products/batch-analyze",
    json={
        "product_names": [
            "Car Phone Holder",
            "Desk Organizer",
            "LED Strip Light",
            "Pet Grooming Tool"
        ]
    }
)

products = response.json()['data']['products']
for p in products:
    print(f"{p['product_name']}: {p['total_score']}/100 ({p['grade']}级)")
```

---

## 🔑 配置API Key（可选）

如果您有OpenAI API Key，可以启用真实AI分析：

### 步骤1：配置API Key

```bash
curl -X POST http://localhost:8000/api/v1/config/api-keys \
  -H "Content-Type: application/json" \
  -d '{
    "openai_api_key": "sk-proj-your-api-key-here"
  }'
```

### 步骤2：验证配置

```bash
curl http://localhost:8000/api/v1/config/status
```

**响应**：
```json
{
  "data": {
    "openai_configured": true,
    "can_use_ai": true,
    "using_mock": false
  }
}
```

**说明**：
- 配置后系统自动启用真实AI分析
- 真实分析耗时更长（5-10分钟）但结果更准确
- Mock数据仍可使用（通过系统设置切换）

---

## 📊 理解评分结果

### 评分维度（100分制）

| 维度 | 分值 | 说明 |
|------|-----|------|
| 市场需求 | 10分 | Google Trends + 数据验证 |
| 功能价值 | 10分 | 解决痛点能力 |
| 情绪价值 | 10分 | 情绪刺激强度 |
| **内容价值** | 15分 | **最关键** 视频内容潜力 |
| 爽点/痛点 | 10分 | S/A/B/C级判定 |
| 美国适配 | 10分 | 30项检查 |
| 尺寸物流 | 10分 | 物流成本占比 |
| 竞争强度 | 10分 | Level 1-5判断 |
| **供应链定价** | 15分 | **关键** 利润率 |

### 等级判定

| 总分 | 等级 | 建议 |
|-----|------|------|
| ≥85分 | **S级** | ✅ 立即测试，优先资源 |
| 75-84分 | **A级** | ✅ 重点测试 |
| 65-74分 | **B级** | ⚠️ 小额测试 |
| 55-64分 | **C级** | ⚠️ 谨慎考虑 |
| <55分 | **D级** | ❌ 不建议 |

---

## 💡 使用技巧

### 1. 快速筛选流程

```
步骤1: 批量快速评分（20个产品）
   ↓
步骤2: 选择分数>75的产品
   ↓
步骤3: 对这些产品进行完整分析
   ↓
步骤4: 查看详细报告，做最终决策
```

### 2. 利润计算

系统自动计算：
- 采购成本
- 物流成本（根据尺寸重量）
- 平台费用（15%）
- 广告成本（20%）
- 退货预留（4%）
- **最终利润率**

**建议**：
- 利润率 >50% = 优秀 ✅
- 利润率 35-50% = 良好 ✅
- 利润率 25-35% = 可接受 ⚠️
- 利润率 <25% = 不建议 ❌

### 3. 竞争度判断

| Level | TikTok视频数 | 建议 |
|-------|------------|------|
| Level 1 | <100 | 🔵 蓝海但需求未验证 |
| Level 2 | 100-500 | 🟢 **黄金窗口期** |
| Level 3 | 500-2000 | 🟡 需要差异化 |
| Level 4 | 2000-5000 | 🟠 红海竞争激烈 |
| Level 5 | >5000 | 🔴 饱和不建议 |

---

## 🐛 常见问题

### Q1: 为什么分析这么快？

**A**: 当前使用Mock数据模式，分析在本地完成。
- Mock模式：2-5秒
- 真实模式（配置API Key后）：5-10分钟

### Q2: Mock数据准确吗？

**A**: Mock数据是基于真实规律生成的模拟数据：
- ✅ 可以用来测试系统功能
- ✅ 可以用来理解评分逻辑
- ❌ 不能用于真实决策
- 💡 配置API Key后可切换到真实数据

### Q3: 如何切换Mock/真实模式？

**A**: 两种方式：
1. 自动切换：配置OpenAI API Key后自动启用真实模式
2. 手动切换：调用 `/api/v1/config/system` 接口

```bash
# 切换到真实模式
curl -X POST http://localhost:8000/api/v1/config/system \
  -H "Content-Type: application/json" \
  -d '{
    "use_mock_data": false,
    "skip_ai_analysis": false
  }'
```

### Q4: 如何查看完整的API文档？

**A**: 访问 http://localhost:8000/docs
- Swagger UI：交互式文档
- 可以直接在线测试所有API

---

## 📖 下一步

### 继续探索

1. **查看完整文档**
   - [API文档](http://localhost:8000/docs)
   - [开发进度](./PROGRESS.md)
   - [项目README](../README.md)

2. **配置真实API**
   - 获取OpenAI API Key
   - 配置到系统
   - 测试真实分析

3. **使用前端界面**
   - 启动前端项目（开发中）
   - 图形化界面操作
   - 更直观的报告展示

---

## 🆘 需要帮助？

- 📝 查看文档：`/docs` 目录
- 🐛 报告问题：GitHub Issues
- 💬 讨论交流：项目Discord/Slack

---

**祝您选品顺利！** 🚀
