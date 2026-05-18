---
name: art-analysis-agent
description: 基于 AG2 的艺术作品分析智能体 - 支持文字和图片分析、色彩分析
category: ai-agents
version: 2.0.0
author: woniuart
tags: [art, analysis, ag2, autogen, multi-agent, vision, color-analysis]
trigger: art analysis|分析艺术|鉴赏|artwork|艺术品|识图|色彩分析
---

# 🎨 Art Analysis Agent - 艺术分析智能体 V2.0

基于 AG2 (AutoGen) 框架的多智能体艺术分析系统。

## 功能

### V2.0 新增功能
- **图片识图分析** - 上传图片，AI 自动识别并分析艺术作品
- **色彩分析** - 提取图片主色调，分析色彩情绪和搭配
- **多模态支持** - 支持文字和图片两种输入方式

### 核心功能
- **Art Analyst** - 艺术分析师：分析视觉元素、构图、技法、象征意义、历史背景
- **Art Critic** - 艺术评论家：审查分析结果、指出不足、提供改进建议
- **飞书机器人集成** - 可接收飞书消息并自动回复分析结果

## 支持的模型

推荐使用支持视觉的多模态模型：

| 模型 | 供应商 | 支持视觉 | 特点 |
|------|--------|----------|------|
| Qwen/Qwen2-VL-72B-Instruct | SiliconFlow | ✅ | 性能强，免费额度多 |
| Qwen/Qwen2-VL-7B-Instruct | SiliconFlow | ✅ | 轻量快速 |
| MiniMaxAI/MiniMax-M2.5 | SiliconFlow | ✅ | 免费额度多 |

## 使用方式

### 方式1: Web 界面（推荐）

启动 Streamlit 界面：

```bash
cd c5-ag2-art-assistant
pip install -r requirements.txt
streamlit run streamlit_app.py
```

访问 http://localhost:8501

功能：
- **文字分析**：输入艺术作品名称，获取详细分析
- **图片分析**：上传艺术作品图片，AI 自动识别并分析
- **色彩分析**：自动提取主色调，分析色彩情绪

### 方式2: 在项目目录运行

```bash
cd c5-ag2-art-assistant
python3 main.py
```

### 方式3: 启动飞书 Bot 服务

```bash
python3 api.py
# 服务运行在 http://localhost:8000
# 飞书回调地址: http://你的域名/feishu/callback
```

## 配置

环境变量在 `.env` 文件中，已预配置 SiliconFlow API：

```
OPENROUTER_API_KEY=sk-mdoklwrqimsbvjnruqrsdxmzoaycpekndmyvqgyymfqwooqa
OPENROUTER_BASE_URL=https://api.siliconflow.cn/v1
AG2_DEFAULT_MODEL=Qwen/Qwen2-VL-72B-Instruct
```

## 示例输入

### 文字分析
```
请分析《蒙娜丽莎》
```

### 图片分析
```
上传一张图片，点击"分析图片"
```

## 输出示例

### 文字分析输出
- 构图与空间处理分析
- 色彩与光影技法
- 人物姿态的象征意义
- 历史与文化语境
- 艺术价值评估

### 图片分析输出
- 画面元素识别
- 构图分析
- 色彩运用分析
- 风格与技法判断
- 色彩情绪分析
- 主色调提取

### 色彩分析输出
- 主色调列表（带颜色预览）
- 颜色名称识别
- 色彩情绪描述
- 色彩搭配建议

## 技术栈

- **前端**: Streamlit
- **后端**: Python + FastAPI
- **AI框架**: AG2 (AutoGen)
- **模型**: SiliconFlow API (支持视觉的大模型)
- **图像处理**: PIL, colorsys