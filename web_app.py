"""
ArtGuide Web App - Flask Web 包装层
用于 Render.com 部署
"""

import asyncio
import os
import threading
from flask import Flask, request, jsonify, render_template_string
from dotenv import load_dotenv

from autogen.beta import Agent
from autogen.beta.config import OpenAIConfig

load_dotenv()

app = Flask(__name__)

# ============ HTML 前端界面 ============
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎨 ArtGuide - 艺术鉴赏AI助手</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Segoe UI', sans-serif; background: #1a1a2e; color: #eee; min-height: 100vh; }
        .container { max-width: 900px; margin: 0 auto; padding: 40px 20px; }
        h1 { text-align: center; font-size: 2.2rem; color: #e2b96f; margin-bottom: 8px; }
        .subtitle { text-align: center; color: #aaa; margin-bottom: 40px; font-size: 1rem; }
        .input-area { display: flex; gap: 12px; margin-bottom: 30px; }
        input[type="text"] {
            flex: 1; padding: 14px 18px; border-radius: 10px; border: 2px solid #333;
            background: #16213e; color: #eee; font-size: 1rem; outline: none;
            transition: border-color 0.3s;
        }
        input[type="text"]:focus { border-color: #e2b96f; }
        button {
            padding: 14px 28px; background: #e2b96f; color: #1a1a2e; border: none;
            border-radius: 10px; font-size: 1rem; font-weight: bold; cursor: pointer;
            transition: background 0.3s;
        }
        button:hover { background: #f0c97a; }
        button:disabled { background: #555; color: #999; cursor: not-allowed; }
        .result-box {
            background: #16213e; border: 1px solid #333; border-radius: 12px;
            padding: 24px; white-space: pre-wrap; line-height: 1.7; min-height: 100px;
            font-size: 0.95rem; display: none;
        }
        .loading { text-align: center; color: #e2b96f; font-size: 1.1rem; display: none; }
        .error { color: #ff6b6b; background: #2d1a1a; padding: 12px; border-radius: 8px; display: none; }
        .examples { margin-bottom: 24px; }
        .examples span { color: #aaa; font-size: 0.9rem; margin-right: 8px; }
        .example-btn {
            background: #0f3460; color: #e2b96f; border: 1px solid #e2b96f;
            padding: 6px 14px; border-radius: 20px; cursor: pointer; font-size: 0.85rem;
            margin: 4px; transition: all 0.2s;
        }
        .example-btn:hover { background: #e2b96f; color: #1a1a2e; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎨 ArtGuide</h1>
        <p class="subtitle">AG2 多智能体艺术鉴赏教学助手</p>

        <div class="examples">
            <span>快速体验：</span>
            <button class="example-btn" onclick="setArtwork('蒙娜丽莎')">蒙娜丽莎</button>
            <button class="example-btn" onclick="setArtwork('星月夜')">星月夜</button>
            <button class="example-btn" onclick="setArtwork('清明上河图')">清明上河图</button>
            <button class="example-btn" onclick="setArtwork('向日葵 梵高')">向日葵</button>
        </div>

        <div class="input-area">
            <input type="text" id="artwork" placeholder="输入艺术作品名称，如：蒙娜丽莎、星月夜、千里江山图..." />
            <button id="analyzeBtn" onclick="analyze()">🔍 分析</button>
        </div>

        <div class="loading" id="loading">⏳ AI 正在分析中，请稍候（约 30-60 秒）...</div>
        <div class="error" id="error"></div>
        <div class="result-box" id="result"></div>
    </div>

    <script>
        function setArtwork(name) {
            document.getElementById('artwork').value = name;
        }

        async function analyze() {
            const artwork = document.getElementById('artwork').value.trim();
            if (!artwork) { alert('请输入艺术作品名称'); return; }

            const btn = document.getElementById('analyzeBtn');
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');
            const error = document.getElementById('error');

            btn.disabled = true;
            loading.style.display = 'block';
            result.style.display = 'none';
            error.style.display = 'none';

            try {
                const resp = await fetch('/analyze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ artwork })
                });
                const data = await resp.json();
                if (data.error) {
                    error.textContent = '错误：' + data.error;
                    error.style.display = 'block';
                } else {
                    result.textContent = data.result;
                    result.style.display = 'block';
                }
            } catch (e) {
                error.textContent = '请求失败：' + e.message;
                error.style.display = 'block';
            } finally {
                btn.disabled = false;
                loading.style.display = 'none';
            }
        }

        document.getElementById('artwork').addEventListener('keypress', e => {
            if (e.key === 'Enter') analyze();
        });
    </script>
</body>
</html>
"""


async def run_artguide(artwork: str) -> str:
    """运行 AG2 多智能体分析"""
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENROUTER_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    model = os.getenv("MODEL_NAME", "gpt-4o-mini")

    if not api_key:
        raise ValueError("未设置 API Key，请在 Render 环境变量中配置 OPENAI_API_KEY")

    config = OpenAIConfig(
        model=model,
        api_key=api_key,
        **({"base_url": base_url} if base_url else {})
    )

    art_analyst = Agent(
        "ArtAnalyst",
        prompt="""你是一位专业的艺术史学者和艺术分析师。你的专长是：
- 分析作品的形式元素：构图、色彩、线条、纹理、光影
- 研究艺术史背景：创作年代、艺术家风格流派、同时代作品比较
- 解读创作技法：油画技法、雕塑手法、媒介特点
- 探索作品象征意义：主题、人物、符号解读
使用专业但易懂的语言，引用具体的艺术史知识，关注对教学有用的细节。""",
        config=config,
    )

    teaching_assistant = Agent(
        "TeachingAssistant",
        prompt="""你是一位大学公共艺术通识课教师，拥有10年教学经验。你专长于：
- 将专业艺术知识转化为学生易理解的内容
- 设计互动式教学问题
- 创建知识框架和记忆点
- 连接艺术作品与当代生活、文化现象
语言生动有趣，使用类比和生活化的例子，包含课堂讨论问题。""",
        config=config,
    )

    coordinator = Agent(
        "ArtGuide_Coordinator",
        prompt="""你是艺术鉴赏教学助手的协调者。
工作流程：1.调用ArtAnalyst工具获取专业艺术分析 2.调用TeachingAssistant将分析转化为教学内容 3.输出整合教学材料
输出格式：作品基本信息、艺术分析要点（3-5个知识点）、教学建议（2-3个讨论问题）、扩展学习资源""",
        config=config,
        tools=[
            art_analyst.as_tool(description="分析艺术作品的构图、色彩、艺术史背景等"),
            teaching_assistant.as_tool(description="将艺术分析转化为适合教学的内容"),
        ],
    )

    reply = await coordinator.ask(
        f"请介绍艺术作品《{artwork}》，包括艺术分析和教学价值。"
    )
    return reply.body


@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    artwork = data.get("artwork", "").strip()
    if not artwork:
        return jsonify({"error": "请输入艺术作品名称"}), 400

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(run_artguide(artwork))
        loop.close()
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "ArtGuide AG2"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
