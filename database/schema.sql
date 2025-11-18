-- AI选品系统 - 数据库结构设计
-- PostgreSQL 15+

-- 清理已存在的表
DROP TABLE IF EXISTS alerts CASCADE;
DROP TABLE IF EXISTS monitoring_records CASCADE;
DROP TABLE IF EXISTS scripts CASCADE;
DROP TABLE IF EXISTS suppliers CASCADE;
DROP TABLE IF EXISTS analysis_results CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TYPE IF EXISTS product_status;
DROP TYPE IF EXISTS alert_type;
DROP TYPE IF EXISTS competition_level;

-- 创建枚举类型
CREATE TYPE product_status AS ENUM ('pending', 'analyzing', 'completed', 'testing', 'active', 'abandoned');
CREATE TYPE alert_type AS ENUM ('trend_up', 'trend_down', 'competition_change', 'price_change');
CREATE TYPE competition_level AS ENUM ('level_1', 'level_2', 'level_3', 'level_4', 'level_5');

-- ==========================================
-- 用户表
-- ==========================================
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- 产品表（核心表）
-- ==========================================
CREATE TABLE products (
    id SERIAL PRIMARY KEY,

    -- 基础信息
    product_name_cn VARCHAR(200),
    product_name_en VARCHAR(200) NOT NULL,
    category VARCHAR(100),
    keywords TEXT[], -- PostgreSQL数组类型

    -- 链接
    alibaba_url TEXT,
    tiktok_url TEXT,
    amazon_url TEXT,

    -- 图片
    images JSONB, -- 存储图片URL数组

    -- 状态
    status product_status DEFAULT 'pending',

    -- 元数据
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    analyzed_at TIMESTAMP,

    -- 索引用字段
    total_score DECIMAL(5,2), -- 总分
    grade VARCHAR(2), -- S/A/B/C/D

    -- 全文搜索
    search_vector tsvector
);

-- ==========================================
-- 分析结果表
-- ==========================================
CREATE TABLE analysis_results (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,

    -- ========== 数据采集结果 ==========
    data_sources JSONB, -- 存储8大数据源的原始数据
    /*
    {
        "alibaba": {
            "sales_7d": 1200,
            "sales_growth": 45.5,
            "suppliers_count": 85,
            "avg_price": 18.50,
            "moq": 30
        },
        "tiktok": {
            "video_count": 350,
            "avg_views": 800000,
            "shop_count": 35,
            "price_range": [14.99, 29.99]
        },
        "google_trends": {
            "score": 65,
            "trend": "rising",
            "related_queries": [...]
        },
        ...
    }
    */

    -- ========== 9大维度评分 ==========

    -- 1. 市场需求 (10分)
    market_demand_score DECIMAL(4,2),
    market_demand_detail JSONB,
    /*
    {
        "google_trends": 65,
        "trend_direction": "rising",
        "data_sources_verified": 4,
        "verification_passed": true
    }
    */

    -- 2. 功能价值 (10分)
    functional_value_score DECIMAL(4,2),
    functional_value_detail JSONB,
    /*
    {
        "pain_point_frequency": "high",
        "pain_point_universality": "universal",
        "pain_point_intensity": "strong",
        "solution_effectiveness": "excellent",
        "visual_effect": "strong",
        "usage_simplicity": "simple"
    }
    */

    -- 3. 情绪价值 (10分)
    emotional_value_score DECIMAL(4,2),
    emotional_value_detail JSONB,
    /*
    {
        "emotion_type": ["visual_pleasure", "healing"],
        "intensity": "extreme",
        "comment_sentiment": 0.92,
        "share_desire": "high"
    }
    */

    -- 4. 内容价值 (15分) - 最重要
    content_value_score DECIMAL(4,2),
    content_value_detail JSONB,
    /*
    {
        "hook_strength": 5,
        "visual_impact": 4,
        "script_count": 12,
        "remix_friendly": 2,
        "ai_generable": 1,
        "breakdown": {
            "hook_strength": 5,
            "visual_impact": 4,
            "script_count": 3,
            "remix_friendly": 2,
            "ai_generable": 1
        }
    }
    */

    -- 5. 爽点/痛点强度 (10分)
    pleasure_pain_score DECIMAL(4,2),
    pleasure_pain_detail JSONB,
    /*
    {
        "type": "cleaning_contrast",
        "level": "S",
        "description": "强烈清洁对比，脏→干净"
    }
    */

    -- 6. 美国市场适配 (10分)
    us_market_fit_score DECIMAL(4,2),
    us_market_fit_detail JSONB,
    /*
    {
        "checklist_passed": 28,
        "checklist_total": 30,
        "issues": [
            {"item": "A3", "desc": "车型适配需调整"}
        ],
        "compliance": {
            "voltage": true,
            "plug": true,
            "fda": true,
            "fcc": true
        }
    }
    */

    -- 7. 尺寸与物流 (10分)
    size_logistics_score DECIMAL(4,2),
    size_logistics_detail JSONB,
    /*
    {
        "dimensions": {"l": 20, "w": 15, "h": 10, "unit": "cm"},
        "weight": 300,
        "volume": 3000,
        "shipping_cost": 4.00,
        "shipping_ratio": 0.16,
        "tier": "small"
    }
    */

    -- 8. 竞争强度 (10分)
    competition_score DECIMAL(4,2),
    competition_detail JSONB,
    /*
    {
        "level": "level_2",
        "tiktok_videos": 350,
        "tiktok_shops": 35,
        "content_similarity": "low",
        "price_war": false,
        "big_brands": false
    }
    */

    -- 9. 供应链与定价 (15分)
    supply_pricing_score DECIMAL(4,2),
    supply_pricing_detail JSONB,
    /*
    {
        "purchase_cost": 3.00,
        "selling_price": 24.99,
        "profit_margin": 0.31,
        "profit_breakdown": {
            "purchase": 3.00,
            "shipping": 4.00,
            "platform_fee": 3.75,
            "ad_cost": 5.00,
            "return_reserve": 1.00,
            "profit": 7.74
        },
        "supplier_maturity": "excellent"
    }
    */

    -- ========== 总分 ==========
    total_score DECIMAL(5,2), -- 总分100分
    grade VARCHAR(2), -- S/A/B/C/D

    -- ========== AI分析结果 ==========
    ai_analysis JSONB,
    /*
    {
        "vision_analysis": {
            "aesthetics": 7,
            "quality_feel": 8,
            "visual_impact": 6,
            "filming_difficulty": "easy"
        },
        "text_analysis": {
            "pain_points": [...],
            "user_sentiment": 0.85,
            "key_features": [...]
        },
        "market_matching": {
            "us_suitable": true,
            "reasons": [...],
            "warnings": [...]
        }
    }
    */

    -- ========== 决策建议 ==========
    recommendation JSONB,
    /*
    {
        "action": "immediate_test",
        "priority": "high",
        "advantages": [...],
        "concerns": [...],
        "next_steps": [...]
    }
    */

    -- 元数据
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- 供应商推荐表
-- ==========================================
CREATE TABLE suppliers (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,

    -- 供应商信息
    supplier_name VARCHAR(200),
    alibaba_url TEXT,

    -- 定价
    price DECIMAL(10,2),
    currency VARCHAR(3) DEFAULT 'CNY',
    moq INTEGER, -- 最小起订量

    -- 评分
    rating DECIMAL(3,2),
    review_count INTEGER,

    -- 服务
    one_piece_dropship BOOLEAN DEFAULT FALSE,
    us_warehouse BOOLEAN DEFAULT FALSE,
    lead_time INTEGER, -- 交期(天)

    -- 优势
    advantages TEXT[],

    -- 排名
    rank INTEGER,

    -- 元数据
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- 脚本库表
-- ==========================================
CREATE TABLE scripts (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,

    -- 脚本信息
    script_type VARCHAR(50), -- 如: "pain_solution", "before_after", "demo"
    title VARCHAR(200),
    description TEXT,

    -- 脚本内容
    script_content JSONB,
    /*
    {
        "hook": "前3秒钩子描述",
        "body": "主体内容",
        "cta": "行动号召",
        "scenes": [
            {
                "time": "0-3s",
                "visual": "视觉描述",
                "text": "文案"
            },
            ...
        ]
    }
    */

    -- 参考视频
    reference_videos JSONB,
    /*
    [
        {
            "url": "tiktok_url",
            "views": 2300000,
            "likes": 180000,
            "comments": 5000
        },
        ...
    ]
    */

    -- 评估
    difficulty VARCHAR(20), -- easy/medium/hard
    expected_effect VARCHAR(20), -- weak/medium/strong/extreme

    -- 元数据
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- 监控记录表
-- ==========================================
CREATE TABLE monitoring_records (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,

    -- 监控数据快照
    snapshot_data JSONB,
    /*
    {
        "tiktok_videos": 350,
        "tiktok_shops": 35,
        "google_trends": 65,
        "alibaba_sales": 1200,
        ...
    }
    */

    -- 变化检测
    changes JSONB,
    /*
    {
        "tiktok_videos": {
            "old": 320,
            "new": 350,
            "change": 30,
            "change_pct": 9.4
        },
        ...
    }
    */

    -- 记录时间
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- 预警表
-- ==========================================
CREATE TABLE alerts (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id),

    -- 预警类型
    alert_type alert_type,

    -- 预警内容
    title VARCHAR(200),
    message TEXT,
    details JSONB,

    -- 严重程度
    severity VARCHAR(20), -- low/medium/high/critical

    -- 状态
    is_read BOOLEAN DEFAULT FALSE,
    read_at TIMESTAMP,

    -- 元数据
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- 索引
-- ==========================================

-- 产品表索引
CREATE INDEX idx_products_status ON products(status);
CREATE INDEX idx_products_grade ON products(grade);
CREATE INDEX idx_products_total_score ON products(total_score DESC);
CREATE INDEX idx_products_user_id ON products(user_id);
CREATE INDEX idx_products_created_at ON products(created_at DESC);
CREATE INDEX idx_products_search_vector ON products USING gin(search_vector);

-- 分析结果表索引
CREATE INDEX idx_analysis_product_id ON analysis_results(product_id);
CREATE INDEX idx_analysis_total_score ON analysis_results(total_score DESC);

-- 供应商表索引
CREATE INDEX idx_suppliers_product_id ON suppliers(product_id);
CREATE INDEX idx_suppliers_rank ON suppliers(rank);

-- 脚本表索引
CREATE INDEX idx_scripts_product_id ON scripts(product_id);
CREATE INDEX idx_scripts_type ON scripts(script_type);

-- 监控记录表索引
CREATE INDEX idx_monitoring_product_id ON monitoring_records(product_id);
CREATE INDEX idx_monitoring_recorded_at ON monitoring_records(recorded_at DESC);

-- 预警表索引
CREATE INDEX idx_alerts_user_id ON alerts(user_id);
CREATE INDEX idx_alerts_product_id ON alerts(product_id);
CREATE INDEX idx_alerts_is_read ON alerts(is_read);
CREATE INDEX idx_alerts_created_at ON alerts(created_at DESC);

-- ==========================================
-- 触发器 - 自动更新时间戳
-- ==========================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_products_updated_at BEFORE UPDATE ON products
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_analysis_updated_at BEFORE UPDATE ON analysis_results
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ==========================================
-- 触发器 - 更新产品表的总分和等级
-- ==========================================

CREATE OR REPLACE FUNCTION update_product_score()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE products
    SET
        total_score = NEW.total_score,
        grade = NEW.grade,
        analyzed_at = CURRENT_TIMESTAMP
    WHERE id = NEW.product_id;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_product_score_trigger
    AFTER INSERT OR UPDATE ON analysis_results
    FOR EACH ROW EXECUTE FUNCTION update_product_score();

-- ==========================================
-- 触发器 - 全文搜索向量更新
-- ==========================================

CREATE OR REPLACE FUNCTION products_search_vector_update()
RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector :=
        setweight(to_tsvector('english', COALESCE(NEW.product_name_en, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(NEW.product_name_cn, '')), 'B') ||
        setweight(to_tsvector('english', COALESCE(NEW.category, '')), 'C');
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER products_search_vector_trigger
    BEFORE INSERT OR UPDATE ON products
    FOR EACH ROW EXECUTE FUNCTION products_search_vector_update();

-- ==========================================
-- 视图 - 产品概览
-- ==========================================

CREATE OR REPLACE VIEW product_overview AS
SELECT
    p.id,
    p.product_name_en,
    p.product_name_cn,
    p.category,
    p.status,
    p.total_score,
    p.grade,
    p.created_at,
    p.analyzed_at,
    a.market_demand_score,
    a.content_value_score,
    a.competition_score,
    a.supply_pricing_score,
    (a.competition_detail->>'level')::TEXT as competition_level,
    (a.supply_pricing_detail->>'profit_margin')::DECIMAL as profit_margin,
    (a.recommendation->>'action')::TEXT as recommended_action,
    (a.recommendation->>'priority')::TEXT as priority
FROM products p
LEFT JOIN analysis_results a ON p.id = a.product_id
ORDER BY p.total_score DESC NULLS LAST;

-- ==========================================
-- 初始数据
-- ==========================================

-- 创建默认用户
INSERT INTO users (username, email, hashed_password, full_name, is_superuser)
VALUES ('admin', 'admin@example.com', 'hashed_password_here', 'Admin User', TRUE);

-- ==========================================
-- 注释
-- ==========================================

COMMENT ON TABLE products IS '产品主表，存储产品基础信息';
COMMENT ON TABLE analysis_results IS '分析结果表，存储AI分析和评分结果';
COMMENT ON TABLE suppliers IS '供应商推荐表';
COMMENT ON TABLE scripts IS '脚本库表，存储TikTok爆款脚本';
COMMENT ON TABLE monitoring_records IS '监控记录表，定时采集产品数据';
COMMENT ON TABLE alerts IS '预警表，重要变化通知';

COMMENT ON COLUMN analysis_results.total_score IS '总分（100分制）';
COMMENT ON COLUMN analysis_results.grade IS '等级：S(85+)/A(75-84)/B(65-74)/C(55-64)/D(<55)';
COMMENT ON COLUMN analysis_results.content_value_score IS '内容价值（15分）- 最关键维度';
COMMENT ON COLUMN analysis_results.supply_pricing_score IS '供应链与定价（15分）- 关键维度';
