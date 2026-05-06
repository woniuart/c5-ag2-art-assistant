# 引用说明 / Attribution

## Fork 源 / Fork Source

本项目基于以下资源构建：

### 主要参考
1. **c5-ag2-hackathon-starter** - Elite20 C5-AG2 挑战启动包
   - 来源: Elite20 训练营
   - 引用内容: 项目结构、AG2 Beta 文档、示例代码模式

2. **AG2 官方文档** (references/ag2_docs/)
   - `20_beta_example_hello_agent.mdx` - 最小可运行示例
   - `11_beta_agents.mdx` - Agent API 和 tool 模式
   - `21_beta_example_research_squad.mdx` - 多 Agent 协作示例
   - 链接: https://docs.ag2.ai/

### 模板文件
- `templates/README_template.md` - README 模板
- `templates/AI_LOG_template.md` - AI 开发日志模板
- `templates/ATTRIBUTION_template.md` - 引用说明模板

## 借鉴片段 / Borrowed Code Snippets

### AG2 Beta Agent 创建模式
```python
agent = Agent(
    "name",
    prompt="...",
    config=config,
)
```
来源: `references/ag2_docs/20_beta_example_hello_agent.mdx`

### Agent-as-Tool 模式
```python
consult_critic = critic.as_tool(
    name="consult_critic",
    description="...",
)
lead.tools.add(consult_critic)
```
来源: `references/ag2_docs/11_beta_agents.mdx`

### 配置加载
```python
from autogen.beta.config import GeminiConfig
config = GeminiConfig(model=model_name, temperature=0.2)
```
来源: AG2 Beta Quickstart

## 创意借鉴 / Creative Inspiration

- **想法来源**: 结合用户的公共艺术教师身份，创建一个艺术分析助手
- **设计参考**: hello_multiagent.py 的 Lead + Critic 双 Agent 模式
- **自定义**: 将艺术分析场景引入多 Agent 协作

---

**声明**: 本项目仅用于教育目的，所有 AG2 代码遵循 Apache 2.0 许可证。