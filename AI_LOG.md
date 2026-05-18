# AI_LOG.md - ArtGuide AG2 开发日志

> 记录本项目开发过程中使用的AI工具和迭代步骤

## 开发概览

- **项目**: ArtGuide - 艺术鉴赏AI助手
- **框架**: AG2 Beta (pyautogen)
- **目标**: 构建多智能体艺术教学系统
- **提交者**: 赵洁

---

## AI 迭代记录

### 第1轮: 需求分析与方案设计

**使用的AI工具**: Claude (Hermes Agent)

**输入**: 
- C5-AG2挑战要求
- 已有的25个AG2 hackathon repo列表
- AG2 Beta文档

**输出**:
- 确定项目方向：艺术鉴赏教学助手
- 设计双Agent协作架构
- 选择multi-agent赛道

**手动步骤**:
- 阅读CHALLENGE.md了解完整要求
- 浏览submitted_repos.md选取参考项目
- 确定使用AG2 Beta框架

---

### 第2轮: 代码框架搭建

**使用的AI工具**: Claude (Hermes Agent)

**输入**:
- AG2 Beta示例代码 (21_beta_example_research_squad.mdx)
- 项目需求说明

**输出**:
- 项目的目录结构
- app.py基础代码框架
- 两个Agent的定义 (ArtAnalyst, TeachingAssistant)

**手动步骤**:
- 创建项目目录
- 编写主程序文件

---

### 第3轮: Agent系统完善

**使用的AI工具**: Claude (Hermes Agent)

**输入**:
- 需要实现的协作模式说明
- Agent角色定义

**输出**:
- 完整的双Agent协作代码
- 使用 `Agent.as_tool()` 实现Agent间调用
- Coordinator协调逻辑

**代码示例**:
```python
# ArtAnalyst: 专业艺术分析
art_analyst = Agent("ArtAnalyst", prompt="...", config=config)

# TeachingAssistant: 教学转化
teaching_assistant = Agent("TeachingAssistant", prompt="...", config=config)

# Coordinator: 协调两个Agent
coordinator = Agent(
    "ArtGuide_Coordinator",
    prompt="...",
    config=config,
    tools=[
        art_analyst.as_tool(description="分析艺术作品"),
        teaching_assistant.as_tool(description="教学转化"),
    ],
)
```

---

### 第4轮: 配置与文档完善

**使用的AI工具**: Claude (Hermes Agent)

**输入**:
- 项目文件结构
- README模板

**输出**:
- requirements.txt
- .env.example
- 完整的README.md

**手动步骤**:
- 验证requirements.txt内容
- 检查.env.example格式

---

### 第5轮: 提交文件生成

**使用的AI工具**: Claude (Hermes Agent)

**输入**:
- 项目已完成的核心文件
- ATTRIBUTION模板

**输出**:
- AI_LOG.md (本文件)
- ATTRIBUTION.md
- 完整的项目文档

---

## 技术亮点

1. **使用AG2 Beta框架**: 采用 `autogen.beta` 而非legacy版本 (+3 Elite20加分)
2. **双Agent协作**: ArtAnalyst + TeachingAssistant 协同工作
3. **Agent-as-Tool模式**: 使用 `Agent.as_tool()` 实现专业分工
4. **教学导向**: 专注于艺术通识课教学场景

## 环境配置记录

```bash
# 创建虚拟环境 (可选)
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或 .venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 配置API密钥
cp .env.example .env
# 编辑 .env 填入 OPENAI_API_KEY
```

---

## 验证检查清单

- [x] 使用 AG2 Beta (`autogen.beta`)
- [x] 至少2个协作Agent
- [x] Agent间通过as_tool调用
- [x] README包含安装说明
- [x] 5分钟内可运行
- [x] 主流程 ≥ 2个Agent协作