# AI选品系统 - TikTok美国站

> 基于数据驱动和AI分析的自动化选品决策系统

## 🎯 系统概述

这是一个高度自动化的TikTok美国站选品系统，能够：
- ✅ 自动采集8大数据源（1688、TikTok、Google Trends等）
- ✅ AI智能分析产品潜力（视觉、内容、市场适配）
- ✅ 自动评分（100分制，9大维度）
- ✅ 自动生成爆款脚本库
- ✅ 自动推荐供应商
- ✅ 持续监控和预警

**核心理念**：输入关键词 → 系统自动分析 → 输出决策

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                      前端界面层                          │
│           React + TailwindCSS + TypeScript              │
└─────────────────────────────────────────────────────────┘
                            ↕️
┌─────────────────────────────────────────────────────────┐
│                      API网关层                           │
│                  FastAPI + Python                       │
└─────────────────────────────────────────────────────────┘
                            ↕️
┌──────────────┬──────────────┬──────────────┬──────────┐
│  数据采集层   │   AI分析层    │   评分引擎   │  监控层  │
├──────────────┼──────────────┼──────────────┼──────────┤
│ • 1688爬虫   │ • 视觉分析   │ • 市场需求   │ • 定时   │
│ • TikTok爬虫 │ • 文本分析   │ • 内容价值   │ • 预警   │
│ • Google API │ • 脚本提取   │ • 竞争分析   │ • 通知   │
│ • Amazon爬虫 │ • 痛点识别   │ • 利润计算   │          │
│ • 其他数据源 │ • 适配判断   │ • 综合评分   │          │
└──────────────┴──────────────┴──────────────┴──────────┘
                            ↕️
┌─────────────────────────────────────────────────────────┐
│                      数据存储层                          │
│              PostgreSQL + Redis + MongoDB               │
└─────────────────────────────────────────────────────────┘
```

---

## 📂 目录结构

```
AI-xuanpinxitong/
├── backend/                    # 后端服务
│   ├── app/
│   │   ├── api/               # API路由
│   │   │   ├── endpoints/     # 各功能端点
│   │   │   └── deps.py        # 依赖注入
│   │   ├── core/              # 核心配置
│   │   │   ├── config.py      # 配置文件
│   │   │   └── security.py    # 安全相关
│   │   ├── models/            # 数据模型
│   │   │   ├── product.py     # 产品模型
│   │   │   ├── analysis.py    # 分析结果模型
│   │   │   └── user.py        # 用户模型
│   │   ├── services/          # 业务逻辑
│   │   │   ├── analysis_service.py   # 分析服务
│   │   │   ├── scoring_service.py    # 评分服务
│   │   │   └── monitor_service.py    # 监控服务
│   │   ├── scrapers/          # 数据采集
│   │   │   ├── alibaba_scraper.py    # 1688爬虫
│   │   │   ├── tiktok_scraper.py     # TikTok爬虫
│   │   │   ├── google_trends.py      # Google Trends
│   │   │   ├── amazon_scraper.py     # Amazon爬虫
│   │   │   └── base_scraper.py       # 基础爬虫类
│   │   ├── ai/                # AI分析
│   │   │   ├── vision_analyzer.py    # 视觉分析
│   │   │   ├── text_analyzer.py      # 文本分析
│   │   │   ├── script_extractor.py   # 脚本提取
│   │   │   └── market_matcher.py     # 市场适配
│   │   └── utils/             # 工具函数
│   │       ├── calculator.py   # 计算工具
│   │       └── helpers.py      # 辅助函数
│   ├── tests/                 # 测试
│   ├── requirements.txt       # 依赖
│   └── main.py               # 入口文件
│
├── frontend/                  # 前端应用
│   ├── src/
│   │   ├── components/       # 组件
│   │   │   ├── ProductCard.tsx
│   │   │   ├── ScoreDisplay.tsx
│   │   │   └── AnalysisReport.tsx
│   │   ├── pages/            # 页面
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Analysis.tsx
│   │   │   └── ProductList.tsx
│   │   ├── services/         # API服务
│   │   │   └── api.ts
│   │   └── utils/            # 工具
│   ├── package.json
│   └── tsconfig.json
│
├── database/                  # 数据库脚本
│   ├── schema.sql            # 数据库结构
│   └── migrations/           # 迁移文件
│
├── scripts/                   # 脚本工具
│   ├── init_db.py            # 初始化数据库
│   └── run_monitor.py        # 运行监控
│
├── docs/                      # 文档
│   ├── ARCHITECTURE.md       # 架构设计
│   ├── API.md               # API文档
│   └── DEPLOYMENT.md        # 部署文档
│
├── .env.example              # 环境变量示例
├── docker-compose.yml        # Docker配置
└── README.md                 # 项目说明
```

---

## 🔧 技术栈

### 后端
- **框架**: FastAPI (高性能异步框架)
- **语言**: Python 3.11+
- **数据库**:
  - PostgreSQL (主数据库)
  - Redis (缓存)
  - MongoDB (非结构化数据)
- **AI/ML**:
  - OpenAI GPT-4 Vision (图像分析)
  - OpenAI GPT-4 (文本分析)
  - LangChain (AI工作流)
- **爬虫**:
  - Playwright (浏览器自动化)
  - BeautifulSoup4 (HTML解析)
  - httpx (异步HTTP客户端)

### 前端
- **框架**: React 18 + TypeScript
- **UI**: TailwindCSS + shadcn/ui
- **状态管理**: Zustand
- **数据获取**: TanStack Query
- **图表**: Recharts

### 基础设施
- **容器化**: Docker + Docker Compose
- **任务队列**: Celery + Redis
- **监控**: Prometheus + Grafana
- **日志**: ELK Stack

---

## 🚀 快速开始（本地运行）

> **推荐**: 使用VS Code打开项目进行开发

### 📥 方式1：本地VS Code开发（推荐，5分钟上手）

**适合**: 想在本地开发和使用的用户

#### 第1步：克隆项目到本地
```bash
git clone https://github.com/yourusername/AI-xuanpinxitong.git
cd AI-xuanpinxitong
```

#### 第2步：使用VS Code打开
```bash
# 在项目目录下打开VS Code
code .
```

#### 第3步：安装Python依赖
在VS Code终端中 (`` Ctrl+` ``):
```bash
cd backend
pip install -r requirements.txt
```

💡 **推荐使用虚拟环境**:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# 然后安装依赖
pip install -r requirements.txt
```

#### 第4步：启动后端
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

看到以下输出即表示成功：
```
✅ INFO:     Uvicorn running on http://0.0.0.0:8000
✅ INFO:     Application startup complete.
```

#### 第5步：打开前端界面
在VS Code中找到 `frontend/index.html` 文件，右键选择 "Open with Live Server"

**或者**直接双击 `frontend/index.html` 用浏览器打开

#### 第6步：开始使用！
1. 在浏览器中会自动打开界面
2. 点击"产品分析"标签
3. 输入产品名称，如 "Car Phone Holder"
4. 点击"开始分析"
5. 2-5秒后查看完整分析报告！

✅ **无需配置API Key** - 系统默认使用Mock数据，全部功能都可以正常使用！

📖 **详细VS Code使用指南**: [docs/VS_CODE_SETUP.md](docs/VS_CODE_SETUP.md)

---

### 📦 方式2：Docker一键启动

**适合**: 想快速体验完整系统的用户

```bash
# 1. 克隆项目
git clone https://github.com/yourusername/AI-xuanpinxitong.git
cd AI-xuanpinxitong

# 2. 一键启动所有服务
docker-compose up -d

# 3. 访问
# API文档: http://localhost:8000/docs
# 前端界面: http://localhost:3000
```

---

### 前置要求

**最小要求** (方式1 - VS Code本地开发):
- ✅ Python 3.11+ - [下载](https://www.python.org/downloads/)
- ✅ VS Code - [下载](https://code.visualstudio.com/)
- ✅ 浏览器（Chrome/Edge/Firefox）

**完整要求** (方式2 - Docker部署):
- ✅ Docker & Docker Compose - [下载](https://www.docker.com/)
- ⚠️ PostgreSQL 15+ (可选，Mock模式不需要)
- ⚠️ Redis 7+ (可选，Mock模式不需要)
- ⚠️ Node.js 18+ (可选，已有HTML前端)

---

## 📊 核心功能

### 1. 快速产品分析
**输入**: 产品关键词或1688链接
**输出**: 完整评估报告（5-10分钟）

**包含**:
- ✅ 100分制评分（9大维度）
- ✅ 竞争分析（Level 1-5）
- ✅ 利润测算
- ✅ 15+爆款脚本
- ✅ TOP 5供应商推荐

### 2. 自动产品发现
**每日自动扫描**:
- 1688跨境热销榜
- TikTok视频增长榜
- Amazon Movers & Shakers
- Shopee东南亚爆款

**输出**: 每日推荐20个潜力产品

### 3. 趋势监控
**自动监控**: 已保存的产品
**频率**: 每日更新
**预警**: 重要变化实时通知

### 4. AI脚本生成
**自动提取**: TikTok爆款视频脚本
**分类整理**: 按类型、难度、效果
**可执行**: 包含拍摄指导

---

## 💯 评分体系

### 9大评分维度（总分100）

| 维度 | 分值 | 说明 |
|------|-----|------|
| 市场需求 | 10分 | Google Trends + 多源验证 |
| 功能价值 | 10分 | AI分析痛点和解决方案 |
| 情绪价值 | 10分 | AI分析评论情绪强度 |
| **内容价值** | 15分 | **核心** AI分析视觉冲击力和脚本潜力 |
| 爽点/痛点强度 | 10分 | AI识别S/A/B/C级 |
| 美国市场适配 | 10分 | 30项自动检查 |
| 尺寸与物流 | 10分 | 自动计算物流成本占比 |
| 竞争强度 | 10分 | Level 1-5判断 |
| **供应链与定价** | 15分 | **关键** 利润率计算 |

### 评分等级

| 总分 | 等级 | 建议 |
|-----|------|------|
| ≥85分 | S级 | 立即测试 |
| 75-84分 | A级 | 重点测试 |
| 65-74分 | B级 | 小额测试 |
| 55-64分 | C级 | 谨慎考虑 |
| <55分 | D级 | 不建议 |

---

## 🗄️ 数据源

系统集成8大数据源：

1. **1688跨境** - 供应链趋势
2. **TikTok** - 内容热度和视频分析
3. **Google Trends** - 搜索趋势
4. **Amazon** - 销量排名变化
5. **Pinterest** - 美国女性用户偏好
6. **Reddit** - 真实用户痛点
7. **Shopee** - 东南亚趋势（领先指标）
8. **Temu** - 低价市场趋势

**三源验证原则**: 至少3个数据源同时验证

---

## 🤖 AI能力

### 视觉分析
- 产品颜值评分
- 质感判断
- 视觉冲击力
- 拍摄难度评估

### 文本分析
- 用户评论情绪分析
- 痛点识别和提取
- 功能价值判断
- 爽点强度评估

### 脚本提取
- 自动分析爆款视频
- 提取脚本模板
- 分类整理（15+类型）
- 生成拍摄指导

### 市场适配
- 自动检查30项指标
- 尺寸适配判断
- 审美匹配度
- 文化适配性

---

## 📈 使用场景

### 场景1: 快速评估新品
```
用户输入: "car phone holder"
         ↓
系统处理: 5-10分钟
         ↓
输出报告: 评分、脚本、供应商
         ↓
用户决策: 2分钟
```
**总耗时: 7-12分钟** (vs 人工2小时)

### 场景2: 每日新品推荐
```
系统自动: 每天凌晨扫描
         ↓
推送通知: 早上9点
         ↓
用户查看: 5分钟浏览20个产品
```
**用户耗时: 5分钟**

### 场景3: 持续监控
```
系统监控: 24/7自动运行
         ↓
发现变化: 自动预警
         ↓
用户响应: 1分钟查看
```
**用户耗时: 1分钟/次**

---

## 🔐 环境变量

创建 `.env` 文件:

```bash
# 数据库
DATABASE_URL=postgresql://user:password@localhost:5432/xuanpin
REDIS_URL=redis://localhost:6379/0
MONGODB_URL=mongodb://localhost:27017/xuanpin

# AI服务
OPENAI_API_KEY=sk-xxxxx

# 数据源API
GOOGLE_TRENDS_API_KEY=xxxxx

# 系统配置
SECRET_KEY=your-secret-key
DEBUG=True
```

---

## 📖 API文档

启动后端后访问:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

主要端点:
- `POST /api/products/analyze` - 分析产品
- `GET /api/products/discover` - 发现新品
- `GET /api/products/{id}` - 获取产品详情
- `GET /api/monitor/alerts` - 获取预警

详细文档: [docs/API.md](docs/API.md)

---

## 🧪 测试

```bash
# 后端测试
cd backend
pytest

# 前端测试
cd frontend
npm test

# E2E测试
npm run test:e2e
```

---

## 📦 部署

### Docker部署 (推荐)
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 传统部署
参见 [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

---

## 🛣️ 开发路线图

### ✅ 第一阶段 (当前)
- [x] 系统架构设计
- [ ] 数据采集模块
- [ ] AI分析引擎
- [ ] 评分系统
- [ ] 基础前端界面

### 🔄 第二阶段
- [ ] 自动监控系统
- [ ] 预警推送
- [ ] 产品对比功能
- [ ] 数据可视化

### 📅 第三阶段
- [ ] 自动化测试工具集成
- [ ] 供应商自动对接
- [ ] AI视频生成
- [ ] 移动端App

---

## 🤝 贡献

欢迎贡献! 请查看 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 许可证

MIT License

---

## 📞 联系方式

- 问题反馈: [GitHub Issues](https://github.com/yourusername/AI-xuanpinxitong/issues)
- 邮箱: your-email@example.com

---

## 🙏 致谢

感谢所有开源项目和社区的支持！

---

**让选品从玄学变成科学！** 🚀
