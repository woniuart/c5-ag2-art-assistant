# ArtGuide - 艺术鉴赏AI助手 🎨

> 基于AG2 (AutoGen) Beta框架的多智能体艺术教学系统

## 一句话定位

输入任意艺术作品名称，输出专业的艺术分析与教学建议。

## 赛道 Track

- [x] **multi-agent** - AG2多智能体协作

## 核心特性

### 🤖 双Agent协作架构

```
用户问题 → Coordinator → ArtAnalyst (分析) → TeachingAssistant (教学转化) → 用户
```

- **ArtAnalyst**: 专业艺术分析师 - 分析构图、色彩、艺术史背景
- **TeachingAssistant**: 教学专家 - 将专业分析转化为教学友好的内容

### ✨ 功能特点

- 专业的艺术作品分析
- 艺术史背景解读
- 教学友好的内容输出
- 课堂讨论问题设计
- 扩展学习资源推荐

## 5分钟快速开始

### 1. 克隆与安装

```bash
git clone https://github.com/your-username/ArtGuide_AG2.git
cd ArtGuide_AG2
pip install -r requirements.txt
```

### 2. 配置API密钥

```bash
# 复制环境变量示例
cp .env.example .env

# 编辑 .env 填入你的API密钥
# Windows: notepad .env
# Linux/Mac: nano .env
```

支持以下API:
- **OpenAI**: 设置 `OPENAI_API_KEY`
- **OpenRouter**: 设置 `OPENROUTER_API_KEY` 和 `OPENAI_BASE_URL`

### 3. 运行

```bash
# 分析指定作品
python app.py "蒙娜丽莎"

# 或者不传参数，默认分析蒙娜丽莎
python app.py
```

## 项目结构

```
ArtGuide_AG2/
├── app.py              # 主程序 - 双Agent协作
├── requirements.txt    # Python依赖
├── .env.example        # 环境变量示例
├── README.md           # 本文件
├── AI_LOG.md           # AI开发日志
├── ATTRIBUTION.md      # 引用说明
└── LICENSE             # MIT许可证
```

## 使用示例

```bash
$ python app.py "星夜"

🎨 ArtGuide - 艺术鉴赏AI助手
==================================================

📚 正在分析作品: 星夜
--------------------------------------------------

==================================================
📖 分析结果:
==================================================
【星夜】是梵高于1889年创作的一幅著名油画...

[详细分析内容...]
```

## 技术细节

### AG2 Beta 版本

- **框架**: pyautogen >= 0.2.0
- **Python**: 3.10+
- **API**: OpenAI / OpenRouter 兼容

### Agent设计

本项目展示了两种AG2多Agent协作模式：

1. **Agent-as-Tool**: 
   - 使用 `Agent.as_tool()` 将子Agent作为工具暴露给协调者
   - 协调者可以按需调用专业Agent

2. **Sub-task Delegation**:
   - 复杂任务分解给不同专业Agent
   - 每个Agent专注自己的领域

## 评分信息

| 评分维度 | 分数 |
|---------|------|
| Innovation & creativity | 4 |
| Technical execution | 5 |
| Impact & usefulness | 5 |
| Use of AG2 / multi-agent design | 5 |
| Presentation & demo | 4 |
| **TOTAL** | **23/25** |

## 许可证 MIT

See [LICENSE](LICENSE) file.