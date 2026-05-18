---
name: art-analysis-agent
description: 基于 AG2 的艺术作品分析智能体 - 双 Agent 协作 (Art Analyst + Art Critic)
category: ai-agents
version: 1.0.0
author: woniuart
tags: [art, analysis, ag2, autogen, multi-agent]
trigger: art analysis|分析艺术|鉴赏|artwork|艺术品
---

# 🎨 Art Analysis Agent - 艺术分析智能体

基于 AG2 (AutoGen) 框架的多智能体艺术分析系统。

## 功能

- **Art Analyst** - 艺术分析师：分析视觉元素、构图、技法、象征意义、历史背景
- **Art Critic** - 艺术评论家：审查分析结果、指出不足、提供改进建议
- **飞书机器人集成** - 可接收飞书消息并自动回复分析结果

## 使用方式

### 方式1: 在项目目录运行

```bash
cd c5-ag2-art-assistant
python3 main.py
```

### 方式2: 启动飞书 Bot 服务

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
AG2_DEFAULT_MODEL=MiniMaxAI/MiniMax-M2.5
```

## 示例输入

```
请分析《蒙娜丽莎》
```

## 输出示例

- 构图与空间处理分析
- 色彩与光影技法
- 神秘微笑的视觉机制
- 人物姿态的象征意义
- 历史与文化语境