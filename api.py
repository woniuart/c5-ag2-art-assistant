"""飞书智能体后端服务 - 艺术鉴赏批评助手

支持功能：
- 接收飞书消息回调
- 调用AG2艺术分析Agent
- 自动回复用户消息

配置方式：
1. 在飞书开放平台创建企业应用
2. 获取 App ID、App Secret
3. 配置服务器URL和回调地址
"""
from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import asyncio
import os
import json
import hmac
import hashlib
import time
import httpx
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="🎨 Art Analysis Feishu Bot",
    description="飞书智能体 - 艺术鉴赏批评助手",
    version="1.0.0"
)

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# ============== 飞书配置 ==============
# 请在飞书开放平台获取并填入
FEISHU_APP_ID = os.getenv("FEISHU_APP_ID", "")
FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET", "")
# 你的公网地址（通过内网穿透或云服务器暴露）
FEISHU_CALLBACK_URL = os.getenv("FEISHU_CALLBACK_URL", "http://localhost:8000")

# 缓存token
_tenant_access_token = None
_token_expires_at = 0

async def get_tenant_access_token():
    """获取飞书tenant_access_token"""
    global _tenant_access_token, _token_expires_at
    
    # 检查缓存的token是否有效
    if _tenant_access_token and time.time() < _token_expires_at:
        return _tenant_access_token
    
    if not FEISHU_APP_ID or not FEISHU_APP_SECRET:
        raise HTTPException(status_code=500, detail="请配置FEISHU_APP_ID和FEISHU_APP_SECRET")
    
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    data = {
        "app_id": FEISHU_APP_ID,
        "app_secret": FEISHU_APP_SECRET
    }
    
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=data)
        result = resp.json()
        
        if result.get("code") != 0:
            raise HTTPException(status_code=500, detail=f"获取token失败: {result}")
        
        _tenant_access_token = result["tenant_access_token"]
        _token_expires_at = time.time() + result.get("expire", 7200) - 300
        return _tenant_access_token


async def send_feishu_message(receive_id: str, message_type: str = "text", content: str = ""):
    """发送飞书消息"""
    token = await get_tenant_access_token()
    
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    params = {"receive_id_type": "open_id"}
    
    # 构建消息内容
    if message_type == "text":
        msg_content = json.dumps({"text": content})
    else:
        msg_content = json.dumps({"text": content})
    
    data = {
        "receive_id": receive_id,
        "msg_type": message_type,
        "content": msg_content
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, params=params, json=data, headers=headers)
        result = resp.json()
        return result


# ============== AG2 Agent 配置 ==============
from autogen.beta import Agent
from autogen.beta.config import OpenAIConfig

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

analyst = None

async def init_agents():
    """初始化Agent"""
    global analyst
    
    analyst = Agent(
        "art_analyst",
        prompt=(
            "你是一位专业的艺术分析师，专门从事视觉艺术分析。"
            "你的角色是提供深入的艺术作品分析，包括：\n"
            "- 视觉构成元素（色彩、线条、形状、空间）\n"
            "- 艺术技法和风格时期\n"
            "- 象征意义和艺术意图\n"
            "- 历史和文化背景\n"
            "提供详细、具有教育意义的简体中文回复。保持友善专业的语气。"
        ),
        config=config,
    )


async def analyze_artwork(artwork_desc: str) -> str:
    """分析艺术作品"""
    if not analyst:
        await init_agents()
    
    prompt = f"请详细分析这件艺术作品：\n{artwork_desc}\n\n请提供至少5个关键见解，包括构图、技法和意义。用优雅的Markdown格式回复。"
    
    reply = await analyst.ask(prompt)
    return reply.body


# ============== API端点 ==============

@app.on_event("startup")
async def startup():
    await init_agents()

@app.get("/")
async def root():
    """返回HTML界面"""
    index_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"name": "Art Analysis Bot", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "ok", "feishu_configured": bool(FEISHU_APP_ID and FEISHU_APP_SECRET)}

@app.post("/analyze")
async def analyze(request: dict):
    """直接分析接口（供测试用）"""
    artwork = request.get("artwork", "")
    if not artwork:
        raise HTTPException(status_code=400, detail="请提供artwork参数")
    
    result = await analyze_artwork(artwork)
    return {"success": True, "result": result}

@app.get("/analyze")
async def analyze_get(q: str = ""):
    """GET方式分析接口（用于公网访问）"""
    if not q:
        raise HTTPException(status_code=400, detail="请提供?q=作品名称参数")
    
    result = await analyze_artwork(q)
    return {"success": True, "result": result}

# ============== 飞书回调接口 ==============

@app.post("/feishu/callback")
async def feishu_callback(request: Request):
    """
    飞书消息回调接口
    
    飞书会POST消息到该接口进行处理
    需要在飞书开放平台配置该回调URL
    """
    body = await request.json()
    
    # 1. 验证URL（飞书首次配置时发送）
    if body.get("type") == "url_verification":
        return {"challenge": body.get("challenge")}
    
    # 2. 事件回调
    if body.get("type") == "event_callback":
        event = body.get("event", {})
        
        # 只处理消息事件
        if event.get("msg_type") == "text":
            message = event.get("message", {})
            
            # 获取发送者open_id和消息内容
            sender_open_id = message.get("sender_id", {}).get("open_id", "")
            user_text = message.get("text", "").strip()
            message_id = message.get("message_id", "")
            
            if not user_text:
                return {"success": True}
            
            # 过滤掉@机器人的前缀（飞书消息格式）
            # 飞书@消息格式: <at id=all></at> 内容
            if "<at" in user_text:
                # 去掉@标签
                import re
                user_text = re.sub(r'<at[^>]*></at>', '', user_text).strip()
            
            print(f"收到消息 from {sender_open_id}: {user_text[:50]}...")
            
            # 调用AI分析
            try:
                analysis_result = await analyze_artwork(user_text)
                
                # 回复用户
                await send_feishu_message(
                    receive_id=sender_open_id,
                    message_type="text",
                    content=analysis_result
                )
                print(f"已回复消息给 {sender_open_id}")
                
            except Exception as e:
                print(f"处理消息失败: {e}")
                await send_feishu_message(
                    receive_id=sender_open_id,
                    message_type="text",
                    content=f"抱歉，分析过程中遇到错误，请稍后再试。\n\n错误信息：{str(e)}"
                )
    
    return {"success": True}


# ============== 配置检查 ==============

@app.get("/feishu/config")
async def check_config():
    """检查飞书配置状态"""
    return {
        "app_id_configured": bool(FEISHU_APP_ID),
        "app_secret_configured": bool(FEISHU_APP_SECRET),
        "callback_url": FEISHU_CALLBACK_URL,
        "full_callback_url": f"{FEISHU_CALLBACK_URL}/feishu/callback"
    }


if __name__ == "__main__":
    import uvicorn
    print("🎨 飞书智能体服务启动中...")
    print(f"📋 飞书回调地址: {FEISHU_CALLBACK_URL}/feishu/callback")
    print("📖 API文档: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)