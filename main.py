"""AG2 Art Analysis Assistant - Multi-Agent Art Analysis System

Two agents collaborate to analyze artworks:
- ARTIST: Provides detailed visual and artistic analysis
- CRITIC: Reviews and critiques the analysis for completeness

Requirements:
    pip install -r requirements.txt
    python3 main.py

"""
from __future__ import annotations
import asyncio
import os
from dotenv import load_dotenv

from autogen.beta import Agent
from autogen.beta.config import OpenAIConfig

load_dotenv()

# Configuration
API_KEY = os.getenv("OPENROUTER_API_KEY", "")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
MODEL = os.getenv("AG2_DEFAULT_MODEL", "google/gemini-2.5-flash")

# Use OpenAI-compatible config with OpenRouter
config = OpenAIConfig(
    model=MODEL,
    api_key=API_KEY,
    base_url=BASE_URL,
    temperature=0.2,
    max_tokens=2048,
)


async def main():
    if not API_KEY:
        print("ERROR: Please set OPENROUTER_API_KEY in .env")
        return

    print("=" * 60)
    print("🎨 AG2 Art Analysis Assistant")
    print("=" * 60)
    print(f"Model: {MODEL}")
    print(f"API: OpenRouter")
    print()

    # Create two cooperating agents
    analyst = Agent(
        "art_analyst",
        prompt=(
            "You are an ART ANALYST specializing in visual arts. "
            "Your role is to provide deep analysis of artworks including:\n"
            "- Visual composition and elements (color, line, shape, space)\n"
            "- Artistic techniques and style period\n"
            "- Symbolic meaning and artistic intent\n"
            "- Historical and cultural context\n"
            "Provide detailed, educational responses in Chinese."
        ),
        config=config,
    )
    
    critic = Agent(
        "art_critic",
        prompt=(
            "You are an ART CRITIC with expertise in art history and theory. "
            "Your role is to review art analyses and provide constructive critique:\n"
            "- Identify gaps or missing information\n"
            "- Suggest additional angles of analysis\n"
            "- Ensure accuracy of art historical claims\n"
            "Be thorough but concise. Respond in Chinese."
        ),
        config=config,
    )

    # Expose CRITIC as a tool for the ANALYST
    consult_critic = critic.as_tool(
        name="consult_critic",
        description="Send analysis to ART CRITIC for review and get feedback",
    )
    
    # Add tool correctly
    if hasattr(analyst.tools, 'append'):
        analyst.tools.append(consult_critic)
    elif hasattr(analyst.tools, 'add'):
        analyst.tools.add(consult_critic)

    # Example: Analyze a famous artwork
    artwork = """
    《蒙娜丽莎》 by Leonardo da Vinci, c. 1503-1519
    Oil on poplar panel, 77 cm × 53 cm
    Located at the Louvre Museum, Paris
    """

    print("🖼️  Analyzing: Mona Lisa by Leonardo da Vinci")
    print("-" * 60)
    
    # Agent 1 provides analysis
    reply = await analyst.ask(
        f"Please analyze this artwork in detail:\n{artwork}\n"
        "Provide at least 5 key insights about composition, technique, and meaning."
    )
    print(reply.body)
    
    print("\n" + "=" * 60)
    print("✅ Analysis complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())