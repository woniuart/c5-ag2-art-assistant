"""
ArtGuide Web App - Flask Web 包装层
用于 Render.com 部署
支持演示模式（无需 API Key）和 AI 模式（需要 API Key）
"""

import asyncio
import os
from flask import Flask, request, jsonify, render_template_string
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DEMO_DATA = {
    "蒙娜丽莎": """🎨 蒙娜丽莎 (Mona Lisa)

📋 基本信息
· 艺术家：列奥纳多·达·芬奇 (Leonardo da Vinci)
· 创作年代：约 1503-1519 年
· 媒介：油画（白杨木板）
· 尺寸：77 cm × 53 cm
· 收藏：法国巴黎卢浮宫

🔬 艺术分析要点
1. 构图技巧：达芬奇运用了"金字塔构图"，蒙娜丽莎的身体形成稳定的三角形，双手交叉置于身前，营造出宁静端庄的视觉效果
2. 晕涂法 (Sfumato)：面部轮廓没有明显的线条边界，色彩和明暗之间柔和过渡，赋予画面朦胧神秘的氛围。这是达芬奇的标志性技法
3. 空气透视：背景的风景从清晰到模糊逐渐变化，暗示了距离感，这是文艺复兴时期开创性的空间表现手法
4. 微笑之谜：嘴角的微妙处理使微笑在不同角度观察时呈现不同表情，至今仍是艺术史上的未解之谜
5. 隐含的数学比例：画面中隐藏着黄金分割比例，体现了文艺复兴对科学美的追求

💬 教学建议
· 课堂讨论1：为什么蒙娜丽莎的微笑让人着迷了500年？你觉得是技术原因还是心理暗示？
· 课堂讨论2：如果用现代摄影技术拍摄一幅"蒙娜丽莎"，你认为能否复制达芬奇作品中的神秘感？为什么？
· 延伸思考：文艺复兴的"人文主义"精神在蒙娜丽莎中是如何体现的？

📚 扩展学习
· 推荐阅读：《达芬奇传》(沃尔特·艾萨克森)
· 相关作品：《最后的晚餐》《维特鲁威人》
· 观看资源：BBC纪录片《达芬奇》""",

    "星月夜": """🎨 星月夜 (The Starry Night)

📋 基本信息
· 艺术家：文森特·梵高 (Vincent van Gogh)
· 创作年代：1889 年 6 月
· 媒介：布面油画
· 尺寸：73.7 cm × 92.1 cm
· 收藏：美国纽约现代艺术博物馆 (MoMA)

🔬 艺术分析要点
1. 笔触语言：梵高使用粗犷有力的短笔触（impasto 厚涂法），颜料层层堆叠，创造出强烈的动感和节奏感，仿佛画面在流动
2. 色彩运用：深蓝色夜空与明黄色星月的强烈对比，形成视觉冲击力。蓝色传达忧郁，黄色象征希望，两者交织反映了画家内心的矛盾
3. 构图动势：画面分为上下两部分——上方旋转的夜空充满动感，下方安静的村庄形成对比。旋涡状的云彩引导视线在画面中运动
4. 柏树象征：前景的柏树如黑色火焰直冲天际，在欧洲传统中柏树象征死亡，但在这里更像是连接大地与星空的桥梁
5. 灵感来源：可能受到葛饰北斋《神奈川冲浪里》的影响，画面中的波浪式旋涡与浮世绘有异曲同工之妙

💬 教学建议
· 课堂讨论1：梵高说"我画星星的时候，总感觉自己在坐摩天轮"，你能从画面中感受到这种"眩晕感"吗？
· 课堂讨论2：这幅画是梵高在精神疗养院期间创作的。艺术创作与精神状态之间是什么关系？
· 延伸思考：后印象派与印象派的根本区别在哪里？

📚 扩展学习
· 推荐阅读：《渴望生活：梵高传》(欧文·斯通)
· 相关作品：《向日葵》《麦田群鸦》《夜间咖啡馆》
· 观看资源：电影《至爱梵高》(Loving Vincent)""",

    "清明上河图": """🎨 清明上河图

📋 基本信息
· 艺术家：张择端 (北宋)
· 创作年代：约 12 世纪初（北宋宣和年间）
· 媒介：绢本设色长卷
· 尺寸：24.8 cm × 528.7 cm
· 收藏：北京故宫博物院

🔬 艺术分析要点
1. 散点透视：不同于西方的焦点透视，中国画的"散点透视"让观者可以像漫步一样沿画卷展开方向观看，视野不受固定视角限制
2. 构图结构：全画分为三段——郊野春光、汴河虹桥、城内街市，由静到动再到繁华，节奏层层递进
3. 细节刻画：画中人物超过 800 人，涵盖各色人物（商人、农民、官员、僧侣、乞丐等），每人都姿态各异、栩栩如生
4. 界画技法：虹桥和建筑的描绘使用了精确的"界画"手法，以界尺为工具绘制直线，保证了建筑的准确性和透视感
5. 历史文献价值：完整记录了北宋汴京（今开封）的城市面貌、商业活动、交通方式和社会风俗，被誉为"中国古代百科全书式画作"

💬 教学建议
· 课堂讨论1：如果要用一幅画来记录你所在城市的日常生活，你会选择画哪些场景？为什么？
· 课堂讨论2：张择端在繁华的市井中隐藏了一些社会问题（如官员出行与百姓争路），你能找出哪些"弦外之音"？
· 延伸思考：中国画"散点透视"的思维方法对现代设计有什么启示？

📚 扩展学习
· 推荐阅读：《北宋汴京的日常生活》《中国画的艺术》
· 相关作品：《千里江山图》(王希孟)、《富春山居图》(黄公望)
· 数字体验：故宫博物院"数字清明上河图"互动展示""",

    "向日葵": """🎨 向日葵 (Sunflowers)

📋 基本信息
· 艺术家：文森特·梵高 (Vincent van Gogh)
· 创作年代：1888 年 8 月
· 媒介：布面油画
· 尺寸：92.1 cm × 73 cm
· 收藏：英国伦敦国家美术馆

🔬 艺术分析要点
1. 色彩革命：梵高抛弃了传统静物画的写实色彩，用大面积的铬黄色作为主色调，配以蓝色背景，创造出前所未有的视觉冲击
2. 笔触肌理：厚涂法让花瓣仿佛从画布上凸起，产生了浮雕般的三维效果。每一笔都充满力量和情感
3. 生命周期隐喻：花瓶中的向日葵呈现不同阶段——有的盛开、有的枯萎、有的结籽，暗示了生命的循环和时间的流逝
4. 黄色执念：梵高认为黄色代表友谊和希望，这组画是他为迎接好友高更来阿尔同居而创作的装饰画
5. 构图张力：简单的花瓶静物却充满动势——花朵向不同方向伸展，画面中蕴含着向外扩张的能量

💬 教学建议
· 课堂讨论1：梵高的向日葵和真实照片中的向日葵，哪个更有"艺术感染力"？为什么？
· 课堂讨论2：这组画的创作背景是梵高和高更的友谊。艺术创作的动机对作品价值有多大影响？
· 延伸思考：为什么梵高的作品生前几乎无人问津，死后却成为无价之宝？

📚 扩展学习
· 推荐阅读：《梵高与高更：电光火石》
· 相关作品：《鸢尾花》《玫瑰》《夜间咖啡馆》
· 趣闻：1987年日本安田火灾海上保险公司以近4000万美元购得《向日葵》，创下当时艺术品拍卖纪录""",
}


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ArtGuide - AG2 艺术鉴赏AI助手</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Segoe UI', -apple-system, sans-serif; background: #0a0a1a; color: #e0e0e0; min-height: 100vh; }
        .container { max-width: 860px; margin: 0 auto; padding: 40px 20px; }
        h1 { text-align: center; font-size: 2.4rem; color: #f0c040; margin-bottom: 6px; letter-spacing: 2px; }
        .subtitle { text-align: center; color: #888; margin-bottom: 36px; font-size: 0.95rem; }
        .mode-badge { text-align: center; margin-bottom: 24px; }
        .mode-badge span { display: inline-block; padding: 4px 16px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; }
        .mode-demo { background: #1a3a2a; color: #4ade80; border: 1px solid #2d5a3d; }
        .mode-ai { background: #1a2a3a; color: #60a5fa; border: 1px solid #2d4a6a; }
        .examples { margin-bottom: 20px; text-align: center; }
        .examples span { color: #777; font-size: 0.85rem; }
        .example-btn {
            background: transparent; color: #f0c040; border: 1px solid #f0c040;
            padding: 6px 16px; border-radius: 20px; cursor: pointer; font-size: 0.85rem;
            margin: 4px; transition: all 0.25s;
        }
        .example-btn:hover { background: #f0c040; color: #0a0a1a; }
        .input-area { display: flex; gap: 12px; margin-bottom: 28px; }
        input[type="text"] {
            flex: 1; padding: 14px 18px; border-radius: 10px; border: 2px solid #222;
            background: #111128; color: #eee; font-size: 1rem; outline: none; transition: border-color 0.3s;
        }
        input[type="text"]:focus { border-color: #f0c040; }
        input[type="text"]::placeholder { color: #555; }
        button.primary {
            padding: 14px 28px; background: #f0c040; color: #0a0a1a; border: none;
            border-radius: 10px; font-size: 1rem; font-weight: bold; cursor: pointer; transition: all 0.3s;
        }
        button.primary:hover { background: #ffd060; transform: translateY(-1px); }
        button.primary:disabled { background: #333; color: #666; cursor: not-allowed; transform: none; }
        .loading { text-align: center; color: #f0c040; font-size: 1.05rem; padding: 30px; display: none; }
        .loading .spinner { display: inline-block; width: 20px; height: 20px; border: 3px solid #333; border-top-color: #f0c040; border-radius: 50%; animation: spin 0.8s linear infinite; margin-right: 10px; vertical-align: middle; }
        @keyframes spin { to { transform: rotate(360deg); } }
        .error { color: #ff6b6b; background: #1a0a0a; border: 1px solid #3a1a1a; padding: 14px; border-radius: 10px; display: none; font-size: 0.9rem; }
        .result-box {
            background: #111128; border: 1px solid #222; border-radius: 14px;
            padding: 28px; white-space: pre-wrap; line-height: 1.8; font-size: 0.95rem; display: none;
            animation: fadeIn 0.4s ease;
        }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .footer { text-align: center; color: #444; font-size: 0.8rem; margin-top: 50px; padding: 20px; border-top: 1px solid #1a1a2a; }
    </style>
</head>
<body>
    <div class="container">
        <h1>ArtGuide</h1>
        <p class="subtitle">AG2 Multi-Agent Art Appreciation Assistant</p>
        <div class="mode-badge"><span class="{{MODE_CLASS}}">{{MODE_TEXT}}</span></div>

        <div class="examples">
            <span>快速体验 :</span>
            <button class="example-btn" onclick="setArtwork('蒙娜丽莎')">蒙娜丽莎</button>
            <button class="example-btn" onclick="setArtwork('星月夜')">星月夜</button>
            <button class="example-btn" onclick="setArtwork('清明上河图')">清明上河图</button>
            <button class="example-btn" onclick="setArtwork('向日葵')">向日葵</button>
        </div>

        <div class="input-area">
            <input type="text" id="artwork" placeholder="输入艺术作品名称，如：蒙娜丽莎、星月夜..." />
            <button class="primary" id="analyzeBtn" onclick="analyze()">分析</button>
        </div>

        <div class="loading" id="loading"><span class="spinner"></span>AI 正在分析中，请稍候...</div>
        <div class="error" id="error"></div>
        <div class="result-box" id="result"></div>

        <div class="footer">Powered by AG2 (AutoGen) | Render Free Tier</div>
    </div>

    <script>
        function setArtwork(name) { document.getElementById('artwork').value = name; }

        async function analyze() {
            const artwork = document.getElementById('artwork').value.trim();
            if (!artwork) return;
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
                    error.textContent = data.error;
                    error.style.display = 'block';
                } else {
                    result.textContent = data.result;
                    result.style.display = 'block';
                }
            } catch (e) {
                error.textContent = 'Network error: ' + e.message;
                error.style.display = 'block';
            } finally {
                btn.disabled = false;
                loading.style.display = 'none';
            }
        }

        document.getElementById('artwork').addEventListener('keypress', e => { if (e.key === 'Enter') analyze(); });
    </script>
</body>
</html>
"""


def is_ai_mode():
    """检查是否配置了 API Key"""
    return bool(os.getenv("OPENAI_API_KEY") or os.getenv("OPENROUTER_API_KEY"))


def get_html():
    """根据模式返回对应的 HTML"""
    if is_ai_mode():
        return HTML_TEMPLATE.replace("{{MODE_CLASS}}", "mode-ai").replace("{{MODE_TEXT}}", "AI Mode")
    else:
        return HTML_TEMPLATE.replace("{{MODE_CLASS}}", "mode-demo").replace("{{MODE_TEXT}}", "Demo Mode (No API Key)")


@app.route("/")
def index():
    return render_template_string(get_html())


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    artwork = data.get("artwork", "").strip()
    if not artwork:
        return jsonify({"error": "请输入艺术作品名称"}), 400

    # 演示模式：使用预设数据
    if not is_ai_mode():
        for key, value in DEMO_DATA.items():
            if key in artwork or artwork in key:
                return jsonify({"result": value})

        demo_msg = (
            f"ArtGuide Demo Mode\n"
            f"{'=' * 40}\n\n"
            f"关于《{artwork}》的展示\n\n"
            f"当前为演示模式（未配置 API Key）。\n"
            f"已内置的演示作品：蒙娜丽莎、星月夜、清明上河图、向日葵\n\n"
            f"如需启用 AI 分析功能，请在 Render 控制台设置环境变量：\n"
            f"  OPENAI_API_KEY = sk-xxx\n"
            f"或\n"
            f"  OPENROUTER_API_KEY = sk-or-xxx\n"
            f"  OPENAI_BASE_URL = https://openrouter.ai/api/v1\n"
        )
        return jsonify({"result": demo_msg})

    # AI 模式：调用 AG2
    try:
        from autogen.beta import Agent
        from autogen.beta.config import OpenAIConfig

        async def run():
            api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENROUTER_API_KEY")
            base_url = os.getenv("OPENAI_BASE_URL")
            model = os.getenv("MODEL_NAME", "gpt-4o-mini")

            config = OpenAIConfig(
                model=model, api_key=api_key,
                **({"base_url": base_url} if base_url else {})
            )

            art_analyst = Agent("ArtAnalyst", prompt=(
                "你是一位专业的艺术史学者和艺术分析师。你的专长是：\n"
                "- 分析作品的形式元素：构图、色彩、线条、纹理、光影\n"
                "- 研究艺术史背景：创作年代、艺术家风格流派\n"
                "- 解读创作技法和象征意义\n"
                "使用专业但易懂的语言，关注对教学有用的细节。"
            ), config=config)

            teaching_assistant = Agent("TeachingAssistant", prompt=(
                "你是一位大学公共艺术通识课教师，拥有10年教学经验。\n"
                "- 将专业艺术知识转化为学生易理解的内容\n"
                "- 设计互动式教学问题\n"
                "- 使用类比和生活化的例子"
            ), config=config)

            coordinator = Agent("ArtGuide_Coordinator", prompt=(
                "你是艺术鉴赏教学助手的协调者。\n"
                "工作流程：1.调用ArtAnalyst获取专业艺术分析 "
                "2.调用TeachingAssistant转化为教学内容 3.输出整合教学材料\n"
                "输出格式：作品基本信息、艺术分析要点（3-5个）、教学建议（2-3个讨论问题）、扩展学习资源"
            ), config=config, tools=[
                art_analyst.as_tool(description="分析艺术作品的构图、色彩、艺术史背景等"),
                teaching_assistant.as_tool(description="将艺术分析转化为适合教学的内容"),
            ])

            reply = await coordinator.ask(f"请介绍艺术作品《{artwork}》，包括艺术分析和教学价值。")
            return reply.body

        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(run())
        loop.close()
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health")
def health():
    mode = "ai" if is_ai_mode() else "demo"
    return jsonify({"status": "ok", "service": "ArtGuide AG2", "mode": mode})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
