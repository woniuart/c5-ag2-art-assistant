# 🎨 Art Analysis Assistant (C5-AG2)

> 一个基于 AG2 (AutoGen) 框架的多智能体艺术分析系统
> A multi-agent art analysis system built with AG2 Beta

## 一句话定位 / One-line

**输入**: 艺术作品信息 → **输出**: 专业艺术分析 + 批评建议

**Input**: Artwork info → **Output**: Professional analysis + critique

## 赛道 / Track

`multi-agent` - 多智能体协作

## 快速开始 / Quick Start

```bash
# 1. 克隆项目
git clone https://github.com/YOUR_USERNAME/c5-ag2-art-assistant.git
cd c5-ag2-art-assistant

# 2. 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env
# 编辑 .env 添加你的 OPENROUTER_API_KEY

# 5. 运行
python main.py
```

获取免费 API Key: https://openrouter.ai/keys

## 核心功能 / Features

- **Art Analyst Agent**: 分析作品的视觉元素、构图、技法、象征意义
- **Art Critic Agent**: 审查并改进分析结果，提供专业批评建议
- **协作模式**: Analyst 调用 Critic 作为工具，实现多轮迭代优化

## 技术栈 / Tech Stack

- **框架**: AG2 Beta (autogen.beta)
- **模型**: Gemini 2.5 Flash (via OpenRouter)
- **运行环境**: Python 3.10+

## 文件结构 / Files

```
├── main.py              # 主程序 - 双 Agent 协作分析
├── requirements.txt     # Python 依赖
├── .env.example         # 环境变量模板
├── README.md            # 本文件
├── AI_LOG.md            # AI 开发日志
└── ATTRIBUTION.md       # 引用说明
```

## 展示 / Demo

[60秒演示视频链接]

## 评分项 / Scoring

| 维度 | 得分 |
|------|------|
| Innovation & creativity | 4 |
| Technical execution | 4 |
| Impact & usefulness | 5 |
| Use of AG2 / multi-agent design | 5 |
| Presentation & demo | 4 |

**总分**: 22 + 加分项

---
Built with ❤️ using AG2 Beta