"""AG2 Art Analysis Assistant - Multi-Agent Art Analysis System

Two agents collaborate to analyze artworks:
- ARTIST: Provides detailed visual and artistic analysis
- CRITIC: Reviews and critiques the analysis for completeness

This demonstrates the AG2 Beta "agent-as-tool" pattern.

Requirements:
    pip install -r requirements.txt
    cp .env.example .env  # Add your OPENROUTER_API_KEY
    python main.py

"""
from __future__ import annotations
import asyncio
import os
from dotenv import load_dotenv

# Try AG2 Beta - fall back to legacy if needed
try:
    from autogen.beta import Agent
    from autogen.beta.config import GeminiConfig
    AG2_BETA = True
except ImportError:
    from autogen import ConversableAgent
    AG2_BETA = False

load_dotenv()

# Configuration
MODEL = os.getenv("AG2_DEFAULT_MODEL", "google/gemini-2.5-flash")
API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# Strip prefix for GeminiConfig
model_name = MODEL.replace("google/", "").replace("anthropic/", "")

if AG2_BETA:
    # Use Gemini config for OpenRouter (supports Gemini models)
    config = GeminiConfig(model=model_name, temperature=0.2)


async def main():
    if not API_KEY:
        print("ERROR: Please set OPENROUTER_API_KEY in .env")
        print("Get one free at: https://openrouter.ai/keys")
        return

    print("=" * 60)
    print("🎨 AG2 Art Analysis Assistant")
    print("=" * 60)
    
    if AG2_BETA:
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
        analyst.tools.add(consult_critic)

        # Example: Analyze a famous artwork
        artwork = """
        《蒙娜丽莎》 by Leonardo da Vinci, c. 1503-1519
        Oil on poplar panel, 77 cm × 53 cm
        Located at the Louvre Museum, Paris
        """

        print("\n🖼️  Analyzing artwork...")
        print("-" * 40)
        
        # Agent 1 provides analysis
        reply = await analyst.ask(
            f"Please analyze this artwork in detail:\n{artwork}\n"
            "Provide at least 5 key insights about composition, technique, and meaning."
        )
        print(reply.body)
        
        # After getting initial analysis, the analyst automatically calls the critic
        # (as defined in their prompt with the tool)
        print("\n" + "=" * 60)
        print("✅ Analysis complete!")
        
    else:
        print("Warning: AG2 Beta not available, using legacy autogen")
        print("This demo requires autogen.beta - please install: pip install ag2>=0.9")


if __name__ == "__main__":
    asyncio.run(main())