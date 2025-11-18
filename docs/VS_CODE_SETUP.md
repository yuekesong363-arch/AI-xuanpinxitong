# VS Code 本地开发指南

> 本指南帮助您在本地使用 VS Code 运行 AI选品系统

---

## 📋 前置要求

在开始之前，请确保您的电脑已安装：

- ✅ **Python 3.11+** - [下载地址](https://www.python.org/downloads/)
- ✅ **VS Code** - [下载地址](https://code.visualstudio.com/)
- ✅ **Git** - [下载地址](https://git-scm.com/)
- ⚠️ **PostgreSQL** (可选，使用Mock模式可跳过)
- ⚠️ **Redis** (可选，使用Mock模式可跳过)

---

## 🚀 快速开始（5分钟）

### 步骤1️⃣：克隆项目

```bash
# 克隆项目到本地
git clone <your-repository-url>

# 进入项目目录
cd AI-xuanpinxitong
```

### 步骤2️⃣：用VS Code打开项目

```bash
# 在当前目录打开VS Code
code .
```

**或者**直接在VS Code中：
1. 点击 `文件` → `打开文件夹`
2. 选择 `AI-xuanpinxitong` 文件夹

### 步骤3️⃣：安装Python依赖

**方式A：使用VS Code终端**
1. 在VS Code中按 `` Ctrl+` `` 打开终端
2. 运行以下命令：

```bash
cd backend
pip install -r requirements.txt
```

**方式B：使用命令行**
```bash
cd AI-xuanpinxitong/backend
pip install -r requirements.txt
```

💡 **推荐**：创建虚拟环境
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

### 步骤4️⃣：启动后端服务

在VS Code终端中运行：

```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

✅ **成功标志**：看到以下输出
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### 步骤5️⃣：打开前端界面

1. 在VS Code中找到 `frontend/index.html` 文件
2. **右键点击** → **选择 "Open with Live Server"**（需要安装Live Server插件）

**或者**直接双击打开 `frontend/index.html` 文件（会用浏览器打开）

✅ **成功标志**：浏览器打开界面，可以看到"AI选品系统"标题

---

## 🎯 第一次使用

### 1️⃣ 查看系统状态

在前端界面中：
1. 点击"系统配置"标签
2. 点击"查看状态"按钮

应该看到：
```
✅ Mock模式已启用
⚠️  OpenAI未配置（使用模拟数据）
```

### 2️⃣ 试用演示分析

**方式A：使用前端界面**
1. 切换到"产品分析"标签
2. 产品名称输入：`Car Phone Holder`
3. 售价输入：`24.99`
4. 点击"开始分析"

**方式B：使用API直接测试**
```bash
curl http://localhost:8000/api/v1/products/demo
```

⏱️ **预计耗时**：2-5秒（Mock模式）

### 3️⃣ 查看分析结果

前端界面会显示：
- ✅ 总分：85/100
- ✅ 等级：A级
- ✅ 建议：重点测试
- ✅ 9个维度的详细评分
- ✅ 利润测算详情
- ✅ 15+爆款脚本
- ✅ TOP 5供应商推荐

---

## 💻 VS Code 推荐插件

为了获得更好的开发体验，建议安装以下插件：

### 必备插件

1. **Python** (Microsoft)
   - 提供Python语法高亮、调试等功能
   - 安装：在VS Code中搜索 "Python"

2. **Pylance** (Microsoft)
   - Python智能提示和类型检查
   - 通常与Python插件一起自动安装

3. **Live Server** (Ritwick Dey)
   - 一键启动本地服务器查看HTML
   - 用于打开 `frontend/index.html`

### 可选插件

4. **REST Client** (Huachao Mao)
   - 在VS Code中直接测试API
   - 可以创建 `.http` 文件测试接口

5. **Thunder Client** (Thunder Client)
   - VS Code内置的Postman替代品
   - 图形化测试API

6. **GitLens** (GitKraken)
   - Git增强工具
   - 查看代码历史、blame等

---

## 🗂️ 项目结构导览

打开VS Code后，您会看到以下结构：

```
AI-xuanpinxitong/
├── backend/                    # 后端代码（重点）
│   ├── main.py                # ⭐ 应用入口
│   ├── app/
│   │   ├── api/v1/endpoints/  # ⭐ API端点
│   │   │   ├── products.py    # 产品分析API
│   │   │   └── config.py      # 配置API
│   │   ├── services/          # ⭐ 核心业务逻辑
│   │   │   ├── analysis_service.py   # 分析服务
│   │   │   ├── scoring_service.py    # 评分引擎
│   │   │   └── config_service.py     # 配置管理
│   │   ├── utils/             # 工具类
│   │   │   ├── mock_data.py   # Mock数据生成
│   │   │   └── calculator.py  # 利润计算器
│   │   └── core/
│   │       └── config.py      # 配置定义
│   ├── .env                   # ⭐ 环境变量配置
│   └── requirements.txt       # Python依赖
├── frontend/                  # 前端代码
│   └── index.html            # ⭐ Web界面
├── database/                  # 数据库
│   └── schema.sql            # 数据库结构
├── docs/                      # 文档
│   ├── QUICK_START.md        # 快速开始
│   ├── VS_CODE_SETUP.md      # 本文档
│   └── PROGRESS.md           # 开发进度
└── README.md                  # 项目说明
```

### 🔑 关键文件说明

| 文件 | 作用 | 何时需要修改 |
|------|------|-------------|
| `backend/.env` | 环境配置 | 配置API Key时 |
| `backend/main.py` | 应用入口 | 添加新路由时 |
| `backend/app/api/v1/endpoints/products.py` | 产品API | 添加新功能时 |
| `backend/app/services/scoring_service.py` | 评分逻辑 | 调整评分规则时 |
| `frontend/index.html` | 用户界面 | 修改界面时 |

---

## 🔧 常用操作

### 启动后端（调试模式）

在VS Code中按 `F5` 启动调试，或者使用终端：

```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**参数说明**：
- `--reload`: 代码修改后自动重启
- `--host 0.0.0.0`: 允许外部访问
- `--port 8000`: 监听8000端口

### 查看API文档

启动后端后，访问：
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 测试单个API

**方式1：使用curl**
```bash
# 健康检查
curl http://localhost:8000/api/v1/products/health

# 演示分析
curl http://localhost:8000/api/v1/products/demo

# 快速评分
curl -X POST http://localhost:8000/api/v1/products/quick-score \
  -H "Content-Type: application/json" \
  -d '{"product_name": "Desk Organizer"}'
```

**方式2：使用Python测试脚本**
```bash
cd backend
python ../test_api.py
```

**方式3：使用REST Client插件**

创建 `test.http` 文件：
```http
### 健康检查
GET http://localhost:8000/api/v1/products/health

### 演示分析
GET http://localhost:8000/api/v1/products/demo

### 快速评分
POST http://localhost:8000/api/v1/products/quick-score
Content-Type: application/json

{
  "product_name": "Car Phone Holder"
}
```

点击 `Send Request` 即可测试

### 查看日志

后端使用 `loguru` 记录日志，所有日志会在终端显示：

```
2024-01-15 10:30:45 | INFO     | 📥 收到分析请求: Car Phone Holder
2024-01-15 10:30:46 | INFO     | 🎯 使用Mock数据模式
2024-01-15 10:30:47 | INFO     | ✅ 分析完成: 85/100 (A级)
```

---

## 🔑 配置 API Key（可选）

### 何时需要配置？

- ✅ 当前使用Mock数据，**无需配置**即可使用全部功能
- ⚠️ 如果需要**真实数据分析**，才需要配置API Key

### 如何配置？

**方式1：使用前端界面（推荐）**

1. 打开 `frontend/index.html`
2. 切换到"系统配置"标签
3. 输入OpenAI API Key
4. 点击"保存配置"

**方式2：修改 .env 文件**

编辑 `backend/.env`：
```bash
# 将 sk-mock-key 替换为真实的 API Key
OPENAI_API_KEY=sk-proj-your-real-api-key-here

# 关闭Mock模式
USE_MOCK_DATA=False
SKIP_AI_ANALYSIS=False
```

**方式3：使用API配置**

```bash
curl -X POST http://localhost:8000/api/v1/config/api-keys \
  -H "Content-Type: application/json" \
  -d '{
    "openai_api_key": "sk-proj-your-real-api-key-here"
  }'
```

### 验证配置

```bash
curl http://localhost:8000/api/v1/config/status
```

应该看到：
```json
{
  "data": {
    "openai_configured": true,
    "can_use_ai": true,
    "using_mock": false
  }
}
```

---

## 🐛 常见问题

### Q1: 无法安装依赖

**问题**：`pip install` 报错

**解决**：
```bash
# 升级pip
python -m pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q2: 端口8000被占用

**问题**：`Address already in use`

**解决**：
```bash
# 方式1：使用其他端口
python -m uvicorn main:app --reload --port 8001

# 方式2：找到并关闭占用8000端口的进程
# Windows
netstat -ano | findstr :8000
taskkill /PID <进程ID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

### Q3: ModuleNotFoundError

**问题**：找不到某个Python模块

**解决**：
```bash
# 确保在backend目录
cd backend

# 重新安装依赖
pip install -r requirements.txt

# 检查是否在虚拟环境中
which python  # macOS/Linux
where python  # Windows
```

### Q4: CORS错误

**问题**：前端无法访问后端API

**解决**：
1. 确保后端使用 `--host 0.0.0.0`
2. 检查 `backend/.env` 中的 `CORS_ORIGINS` 配置
3. 如果使用Live Server，确保端口号在CORS允许列表中

### Q5: 前端显示空白

**问题**：打开 `index.html` 后页面空白

**解决**：
1. 按 `F12` 打开浏览器开发者工具
2. 查看 Console 标签是否有错误
3. 确保后端正在运行（访问 http://localhost:8000/docs）
4. 检查 `index.html` 中的 API_BASE_URL 是否正确

---

## 🎓 学习路径

### 新手入门（第1天）

1. ✅ 成功启动后端
2. ✅ 打开前端界面
3. ✅ 运行演示分析
4. ✅ 理解评分结果

### 熟悉系统（第2-3天）

1. 📖 阅读 `docs/QUICK_START.md`
2. 🔍 浏览API文档 http://localhost:8000/docs
3. 🧪 测试所有API端点
4. 📊 分析自己的产品

### 深入理解（第4-7天）

1. 📁 阅读 `backend/app/services/scoring_service.py` - 理解评分逻辑
2. 📁 阅读 `backend/app/utils/calculator.py` - 理解利润计算
3. 📁 阅读 `backend/app/utils/mock_data.py` - 理解数据结构
4. 🔧 尝试调整评分权重
5. 🔧 尝试修改前端界面

### 高级开发（第2周+）

1. 🗄️ 配置真实数据库（PostgreSQL + Redis）
2. 🤖 集成真实OpenAI API
3. 🕷️ 实现真实数据爬虫
4. 📈 添加新的分析维度
5. 🎨 优化前端界面

---

## 📚 相关文档

- [快速开始指南](./QUICK_START.md) - 系统功能介绍
- [开发进度](./PROGRESS.md) - 已完成和待开发功能
- [API文档](http://localhost:8000/docs) - 完整API参考
- [项目README](../README.md) - 项目概述

---

## 🆘 获取帮助

### 遇到问题？

1. 📖 查看本文档的"常见问题"部分
2. 📖 查看 `docs/QUICK_START.md`
3. 🐛 在GitHub创建Issue
4. 💬 加入项目社区讨论

### 反馈建议

如果您有任何建议或发现Bug，欢迎：
- 🐛 提交Issue
- 🔧 提交Pull Request
- 💬 参与讨论

---

## ✅ 检查清单

在开始开发前，确保您已完成：

- [ ] 安装了Python 3.11+
- [ ] 安装了VS Code
- [ ] 克隆了项目代码
- [ ] 安装了Python依赖
- [ ] 成功启动了后端（看到Uvicorn运行提示）
- [ ] 成功打开了前端界面
- [ ] 运行了演示分析并看到结果
- [ ] 了解了项目结构
- [ ] 知道如何查看API文档

---

**祝您开发愉快！** 🚀

如有任何问题，请随时查阅文档或寻求帮助。
