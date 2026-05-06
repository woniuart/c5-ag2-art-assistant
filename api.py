"""FastAPI Web Service for Art Analysis Assistant
将多智能体艺术分析服务变成REST API

运行方式:
    pip install -r requirements.txt fastapi uvicorn
    python3 api.py

服务地址: http://localhost:8000
API文档: http://localhost:8000/docs
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import asyncio
import os
from dotenv import load_dotenv

from autogen.beta import Agent
from autogen.beta.config import OpenAIConfig

load_dotenv()

app = FastAPI(
    title="🎨 Art Analysis API",
    description="多智能体艺术分析助手 - 飞书智能体后端服务",
    version="1.0.0"
)

# ============== 配置 ==============
API_KEY = os.getenv("OPENROUTER_API_KEY", "")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
MODEL = os.getenv("AG2_DEFAULT_MODEL", "google/gemini-2.5-flash")

config = OpenAIConfig(
    model=MODEL,
    api_key=API_KEY,
    base_url=BASE_URL,
    temperature=0.2,
    max_tokens=4096,
)

# ============== Agent 初始化 ==============
analyst = None
critic = None

async def init_agents():
    """初始化 Agent"""
    global analyst, critic
    
    analyst = Agent(
        "art_analyst",
        prompt=(
            "你是一位专业的艺术分析师，专门从事视觉艺术分析。"
            "你的角色是提供深入的艺术作品分析，包括：\n"
            "- 视觉构成元素（色彩、线条、形状、空间）\n"
            "- 艺术技法和风格时期\n"
            "- 象征意义和艺术意图\n"
            "- 历史和文化背景\n"
            "提供详细、具有教育意义的简体中文回复。"
        ),
        config=config,
    )
    
    critic = Agent(
        "art_critic",
        prompt=(
            "你是一位艺术评论家，精通艺术史和艺术理论。"
            "你的职责是审查艺术分析并提供建设性批评：\n"
            "- 识别分析中的空白或遗漏信息\n"
            "- 建议额外的分析角度\n"
            "- 确保艺术史论断的准确性\n"
            "回复要详尽但简洁，使用简体中文。"
        ),
        config=config,
    )
    
    # 将 CRITIC 作为工具暴露给 ANALYST
    consult_critic = critic.as_tool(
        name="consult_critic",
        description="发送分析给艺术评论家审查并获取反馈",
    )
    
    if hasattr(analyst.tools, 'append'):
        analyst.tools.append(consult_critic)

# ============== 请求模型 ==============
class AnalyzeRequest(BaseModel):
    """艺术分析请求"""
    artwork: str  # 艺术作品描述/名称/图片URL
    user_id: Optional[str] = None  # 可选：用户ID
    language: Optional[str] = "zh"  # 语言：zh/en

class HealthResponse(BaseModel):
    """健康检查响应"""
    status: str
    model: str
    agent_initialized: bool

# ============== API 端点 ==============

@app.on_event("startup")
async def startup_event():
    """服务启动时初始化 Agent"""
    await init_agents()

@app.get("/", tags=["Root"])
async def root():
    """根路径"""
    return {
        "name": "Art Analysis API",
        "version": "1.0.0",
        "description": "多智能体艺术分析助手",
        "docs": "/docs"
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """健康检查"""
    return HealthResponse(
        status="ok",
        model=MODEL,
        agent_initialized=True
    )

@app.post("/analyze", tags=["Analysis"])
async def analyze_artwork(request: AnalyzeRequest):
    """
    分析艺术作品
    
    请求体:
    ```json
    {
        "artwork": "《蒙娜丽莎》by Leonardo da Vinci",
        "user_id": "optional_user_id",
        "language": "zh"
    }
    ```
    
    返回:
    ```json
    {
        "success": true,
        "result": "艺术分析内容...",
        "artwork": "输入的艺术作品描述"
    }
    ```
    """
    if not ANALYST:
        raise HTTPException(status_code=503, detail="Agent未初始化，请稍后重试")
    
    if not request.artwork.strip():
        raise HTTPException(status_code=400, detail="请提供艺术作品描述")
    
    try:
        prompt = f"请详细分析这件艺术作品：\n{request.artwork}\n\n请提供至少5个关键见解，包括构图、技法和意义。"
        
        # 调用 Agent 分析
        reply = await analyst.ask(prompt)
        
        return {
            "success": True,
            "result": reply.body,
            "artwork": request.artwork
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")

# ============== 飞书机器人 Webhook 端点 ==============

@app.post("/feishu/webhook", tags=["Feishu"])
async def feishu_webhook(request: dict):
    """
    飞书机器人 Webhook 端点
    
    飞书机器人发送消息时会POST到该端点
    需要在飞书后台配置 Webhook URL
    """
    try:
        # 解析飞书消息
        event = request.get("event", {})
        message = event.get("message", {})
        message_type = message.get("message_type", "")
        
        # 文本消息
        if message_type == "text":
            text_content = message.get("text", {}).get("content", "").strip()
            
            if not text_content:
                return {"success": True}
            
            # 调用分析服务
            reply = await analyst.ask(
                f"请详细分析这件艺术作品：\n{text_content}\n\n请提供至少5个关键见解。"
            )
            
            # 返回响应（需要飞书应用支持被动回复消息）
            return {
                "success": True,
                "msg_type": "text",
                "content": {"text": reply.body}
            }
        
        return {"success": True, "message": "仅支持文本消息"}
        
    except Exception as e:
        return {"success": False, "error": str(e)}

# 保持全局变量引用
ANALYST = None

# 启动时初始化
import atexit
@atexit.register
def cleanup():
    pass

if __name__ == "__main__":
    import uvicorn
    print("🎨 Art Analysis API 服务启动中...")
    print("📖 API文档: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)