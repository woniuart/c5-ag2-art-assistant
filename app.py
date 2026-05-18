"""
ArtGuide - AG2多智能体艺术鉴赏教学助手
Multi-agent Art Appreciation Teaching Assistant

两个协作Agent:
1. ArtAnalyst - 分析艺术作品的构图、色彩、艺术史背景
2. TeachingAssistant - 将分析结果转化为适合教学的内容

运行方式:
    python app.py "蒙娜丽莎"
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

from autogen.beta import Agent
from autogen.beta.config import OpenAIConfig

# 加载环境变量
load_dotenv()


async def main():
    """主函数：初始化并运行多智能体艺术鉴赏系统"""
    
    # 获取API配置 - 支持多种模型
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENROUTER_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")  # 用于OpenRouter等第三方
    model = os.getenv("MODEL_NAME", "gpt-4o-mini")
    
    if not api_key:
        print("错误: 请设置环境变量 OPENAI_API_KEY 或 OPENROUTER_API_KEY")
        print("如何设置:")
        print("  Windows: set OPENAI_API_KEY=your_key")
        print("  Linux/Mac: export OPENAI_API_KEY=your_key")
        sys.exit(1)
    
    # 配置模型
    if base_url:
        config = OpenAIConfig(
            model=model,
            api_key=api_key,
            base_url=base_url,
        )
    else:
        config = OpenAIConfig(
            model=model,
            api_key=api_key,
        )
    
    print("🎨 ArtGuide - 艺术鉴赏AI助手")
    print("=" * 50)
    
    # ============ Agent 1: ArtAnalyst ============
    # 艺术分析师：分析作品的艺术元素、历史背景、创作技法
    art_analyst = Agent(
        "ArtAnalyst",
        prompt="""
你是一位专业的艺术史学者和艺术分析师。你的专长是：
- 分析作品的形式元素：构图、色彩、线条、纹理、光影
- 研究艺术史背景：创作年代、艺术家风格流派、同时代作品比较
- 解读创作技法：油画技法、雕塑手法、媒介特点
- 探索作品象征意义：主题、人物、符号解读

你的回答应该：
- 使用专业但易懂的语言
- 引用具体的艺术史知识
- 关注对教学有用的细节
- 保持学术严谨性
""",
        config=config,
    )
    
    # ============ Agent 2: TeachingAssistant ============
    # 教学助手：将艺术分析转化为适合教学的内容
    teaching_assistant = Agent(
        "TeachingAssistant",
        prompt="""
你是一位大学公共艺术通识课教师，拥有10年教学经验。你专长于：
- 将专业艺术知识转化为学生易理解的内容
- 设计互动式教学问题
- 创建知识框架和记忆点
- 连接艺术作品与当代生活、文化现象

你的回答应该：
- 语言生动有趣，吸引学生兴趣
- 使用类比和生活化的例子
- 包含可课堂讨论的问题
- 提供进一步学习的线索
- 适合通识课教学场景
""",
        config=config,
    )
    
    # 创建主协调agent，使用Agent.as_tool()进行协作
    coordinator = Agent(
        "ArtGuide_Coordinator",
        prompt="""
你是艺术鉴赏教学助手的协调者。用户会询问关于艺术作品的问题。

你的工作流程：
1. 首先调用 ArtAnalyst 工具获取专业的艺术分析
2. 然后调用 TeachingAssistant 工具将分析转化为教学友好的内容
3. 最终输出整合后的教学材料

输出格式：
- 作品基本信息（名称、艺术家、年代、媒介）
- 艺术分析要点（3-5个核心知识点）
- 教学建议（2-3个课堂讨论问题）
- 扩展学习资源

始终保持友好、专业的态度。
""",
        config=config,
        tools=[
            art_analyst.as_tool(
                description="分析艺术作品的构图、色彩、艺术史背景等"
            ),
            teaching_assistant.as_tool(
                description="将艺术分析转化为适合教学的内容"
            ),
        ],
    )
    
    # 获取用户输入
    artwork = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "蒙娜丽莎"
    
    print(f"\n📚 正在分析作品: {artwork}")
    print("-" * 50)
    
    # 运行协调者
    reply = await coordinator.ask(
        f"请介绍艺术作品《{artwork}》，包括艺术分析和教学价值。"
    )
    
    print("\n" + "=" * 50)
    print("📖 分析结果:")
    print("=" * 50)
    print(reply.body)


if __name__ == "__main__":
    asyncio.run(main())