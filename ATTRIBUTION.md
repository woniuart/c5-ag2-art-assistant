# ATTRIBUTION.md - 引用与借鉴说明

> 记录本项目中引用、借鉴的开源项目、文档和代码片段

---

## 项目来源

### 直接Fork/参考的Repo

本项目**不是直接fork**自已有的25个hackathon repo，而是：
- 参考了多个repo的设计模式
- 基于AG2 Beta官方文档重新构建
- 针对艺术教学场景定制

---

## 借鉴来源

### 1. AG2官方文档

**来源**: `c5-ag2-hackathon-starter/references/ag2_docs/`

- `21_beta_example_research_squad.mdx` - 多Agent协作模式参考
- `20_beta_example_hello_agent.mdx` - 最小可运行示例
- `11_beta_agents.mdx` - Agent类API设计
- `30_beta_tools_builtin.mdx` - 工具系统

**借鉴内容**:
```python
# 参考: 21_beta_example_research_squad.mdx
# Agent.as_tool() 模式
math_expert = Agent("math-expert", prompt=..., config=config)
coordinator = Agent(
    "coordinator",
    prompt=...,
    config=config,
    tools=[math_expert.as_tool(description="...")]
)
```

### 2. 挑战模板

**来源**: `c5-ag2-hackathon-starter/templates/`

- `AI_LOG_template.md` - AI开发日志模板
- `ATTRIBUTION_template.md` - 引用说明模板

---

## 代码片段引用

### Agent定义模式

```python
# 来源: AG2 Beta官方示例
# 文件: 21_beta_example_research_squad.mdx (行47-75)

from autogen.beta import Agent
from autogen.beta.config import OpenAIConfig, GeminiConfig

agent = Agent(
    "agent_name",
    prompt="You are...",
    config=OpenAIConfig(model="gpt-4o-mini", api_key=api_key),
)
```

### Tool暴露模式

```python
# 来源: AG2 Beta官方示例
# 文件: 21_beta_example_research_squad.mdx (行117-122)

tools=[
    agent.as_tool(description="Delegate to this agent")
]
```

### 异步运行模式

```python
# 来源: AG2 Beta官方示例
import asyncio
from autogen.beta import Agent

async def main():
    agent = Agent(...)
    reply = await agent.ask("question")
    print(reply.body)

asyncio.run(main())
```

---

## 创新之处

虽然借鉴了官方示例，但本项目有如下独特设计：

1. **领域专业化**: 
   - 专注于艺术鉴赏与教学
   - ArtAnalyst: 艺术史学者角色
   - TeachingAssistant: 大学教师角色

2. **教学导向输出**: 
   - 包含课堂讨论问题
   - 扩展学习资源推荐
   - 知识框架构建

3. **中文语境**: 
   - 全中文prompt设计
   - 面向中国艺术教育场景

---

## 许可证

- 本项目代码: [MIT License](LICENSE)
- AG2框架: Apache 2.0
- 模板文件: MIT License

---

*本项目为Elite20 C5-AG2挑战提交作品*
*作者: 赵洁*
*日期: 2026-05-06*