import streamlit as st
import os
import base64
import io
import json
from dotenv import load_dotenv
from PIL import Image
import colorthon

# 加载.env文件
load_dotenv()

# ========== 配置 ==========
API_KEY = os.getenv("OPENROUTER_API_KEY", "")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://api.siliconflow.cn/v1")
MODEL = os.getenv("AG2_DEFAULT_MODEL", "MiniMaxAI/MiniMax-M2.5")
VISION_MODEL = os.getenv("VISION_MODEL", "Qwen/Qwen2-VL-7B-Instruct")
# 如果用 OpenRouter 做视觉分析（更稳定），可设置：
# VISION_MODEL = "google/gemini-2.0-flash-001"
# VISION_BASE_URL = "https://openrouter.ai/api/v1"

# ========== Page config ==========
st.set_page_config(
    page_title="🎨 艺术分析助手",
    page_icon="🎨",
    layout="wide"
)

# 隐藏Streamlit默认的菜单和footer
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ========== 标题 ==========
st.markdown("""
<style>
.title {
    text-align: center;
    font-size: 3em;
    background: linear-gradient(90deg, #ff6b6b, #feca57, #48dbfb, #ff9ff3);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="title">🎨 艺术分析助手</h1>', unsafe_allow_html=True)
st.markdown("### 基于 **多智能体 AI** | 支持文字分析 · 图片识图 · 色彩分析")
st.markdown("---")

# ========== 检查API配置 ==========
if not API_KEY:
    st.error("⚠️ 未配置 API Key！请在 .env 文件中设置 OPENROUTER_API_KEY")
    st.info("当前使用 SiliconFlow API，请在 .env 中填写你的 API Key")
    st.stop()

# ========== 侧边栏：模式选择 ==========
with st.sidebar:
    st.header("⚙️ 设置")
    analysis_mode = st.radio(
        "分析模式",
        ["📝 文字输入分析", "📷 上传图片识图", "🎨 图片色彩分析"],
        index=0
    )
    st.markdown("---")
    st.markdown("**当前模型**")
    st.code(MODEL)
    st.markdown("**视觉模型**")
    st.code(VISION_MODEL)

# ========== 辅助函数 ==========
def image_to_base64(image: Image.Image, max_size: int = 512) -> str:
    """将 PIL 图片转为 base64 字符串（压缩到合适大小）"""
    img = image.copy()
    img.thumbnail((max_size, max_size), Image.LANCZOS)
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=85)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def extract_colors(image: Image.Image, num_colors: int = 6):
    """提取图片主色调"""
    try:
        import colorthief
        ct = colorthief.ColorThief(image)
        palette = ct.get_palette(color_count=num_colors)
        dominant = ct.get_color(quality=1)
        return palette, dominant
    except Exception:
        # fallback：使用 PIL 简单采样
        img = image.copy()
        img.thumbnail((100, 100))
        pixels = list(img.getdata())
        # 简单统计出现最多的颜色
        from collections import Counter
        counter = Counter(pixels)
        palette = [c for c, _ in counter.most_common(num_colors)]
        dominant = palette[0] if palette else (0, 0, 0)
        return palette, dominant


def hex_to_rgb(hex_color: str):
    """hex 转 rgb"""
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    """rgb 转 hex"""
    return "#{:02x}{:02x}{:02x}".format(
        max(0, min(255, rgb[0])),
        max(0, min(255, rgb[1])),
        max(0, min(255, rgb[2]))
    )


def analyze_image_with_vision(image_b64: str, prompt: str) -> str:
    """调用视觉大模型分析图片"""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

        messages = [
            {"role": "system", "content": "你是一位专业的艺术史学者和视觉艺术分析师，擅长从图像中分析艺术作品。请用简体中文详细回复，格式清晰，适合教学使用。"},
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
            ]}
        ]

        response = client.chat.completions.create(
            model=VISION_MODEL,
            messages=messages,
            max_tokens=2000,
            temperature=0.3,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"视觉分析出错: {str(e)}"


def analyze_text(artwork: str) -> str:
    """文字输入分析（原有功能）"""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": """你是一位专业的艺术分析师，专门从事视觉艺术分析。

请详细分析艺术作品，包括：
1. 构图与空间处理
2. 色彩运用与光影
3. 技法与风格特点
4. 象征意义与主题
5. 历史背景与文化语境

请提供详细、具有教育意义的简体中文回复。使用清晰的Markdown格式。"""},
                {"role": "user", "content": f"请详细分析这件艺术作品：《{artwork}》，提供至少5个关键见解。用中文回复。"}
            ],
            temperature=0.2,
            max_tokens=4000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"分析出错: {str(e)}"


# ========== 主界面 ==========

if analysis_mode == "📝 文字输入分析":
    st.markdown("## 📝 文字输入分析")
    col1, col2 = st.columns([3, 1])
    with col1:
        artwork = st.text_input(
            "请输入艺术作品名称",
            placeholder="如：蒙娜丽莎、星空、向日葵、最后的晚餐",
            label_visibility="collapsed",
            key="text_input"
        )
    with col2:
        analyze_btn = st.button("🎨 开始分析", use_container_width=True, key="text_btn")

    # 示例按钮
    st.markdown("💡 **快速示例：**")
    examples = ["蒙娜丽莎", "星空", "向日葵", "格尔尼卡", "千里江山图"]
    cols = st.columns(len(examples))
    for i, ex in enumerate(examples):
        if cols[i].button(ex, key=f"ex_{i}"):
            artwork = ex
            analyze_btn = True

    if analyze_btn and artwork:
        with st.spinner(f"🎨 AI 正在分析《{artwork}》，请稍候..."):
            result = analyze_text(artwork)
        st.markdown("---")
        st.markdown(result)
        st.markdown("---")
        st.success("✅ 分析完成！")

elif analysis_mode == "📷 上传图片识图":
    st.markdown("## 📷 上传图片识图")
    st.markdown("上传艺术作品的图片，AI 将自动识别并分析该作品。")

    uploaded_file = st.file_uploader(
        "选择一张艺术作品图片",
        type=["jpg", "jpeg", "png", "webp"],
        key="vision_uploader"
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        col_img, col_info = st.columns([1, 2])

        with col_img:
            st.image(image, caption="上传的图片", use_column_width=True)

        with col_info:
            st.markdown("**图片信息**")
            st.write(f"- 尺寸：{image.size[0]} × {image.size[1]} px")
            st.write(f"- 格式：{uploaded_file.type}")

            analyze_vision_btn = st.button("🔍 开始识图分析", use_container_width=True, key="vision_btn")

        if analyze_vision_btn:
            with st.spinner("🤖 视觉AI正在识别并分析图片，请稍候（约30秒）..."):
                image_b64 = image_to_base64(image, max_size=512)
                prompt = """请识别并分析这张艺术作品图片。

请按以下结构回复（用简体中文）：

## 📋 作品识别
- 作品名称（如能识别）
- 艺术家
- 创作年代（如能判断）
- 艺术流派

## 🔬 艺术分析
1. 构图与空间处理
2. 色彩运用与光影效果
3. 技法与风格特点
4. 象征意义与主题表达
5. 历史背景与文化语境

## 💬 教学建议
- 2-3个适合课堂讨论的问题
- 延伸学习资源推荐

请详细、专业、具有教育意义。"""
                result = analyze_image_with_vision(image_b64, prompt)

            st.markdown("---")
            st.markdown(result)
            st.markdown("---")
            st.success("✅ 识图分析完成！")

elif analysis_mode == "🎨 图片色彩分析":
    st.markdown("## 🎨 图片色彩分析")
    st.markdown("上传艺术作品图片，AI 将提取主色调并进行专业色彩分析。")

    uploaded_file = st.file_uploader(
        "选择一张艺术作品图片",
        type=["jpg", "jpeg", "png", "webp"],
        key="color_uploader"
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        col_img, col_color = st.columns([1, 2])

        with col_img:
            st.image(image, caption="上传的图片", use_column_width=True)

        with col_color:
            num_colors = st.slider("提取主色数量", min_value=3, max_value=10, value=6)

            analyze_color_btn = st.button("🎨 开始色彩分析", use_container_width=True, key="color_btn")

        if analyze_color_btn:
            with st.spinner("🎨 正在提取色彩并分析..."):
                # 提取主色调
                palette, dominant = extract_colors(image, num_colors)

                # 显示色彩面板
                st.markdown("### 🎨 主色调提取")
                color_html = "<div style='display:flex; gap:8px; flex-wrap:wrap; margin:10px 0;'>"
                for rgb in palette:
                    hex_c = rgb_to_hex(rgb)
                    color_html += f"<div style='width:60px;height:60px;background:{hex_c};border-radius:8px;border:1px solid #555;' title='{hex_c} RGB{rgb}'></div>"
                color_html += "</div>"
                st.markdown(color_html, unsafe_allow_html=True)

                # 主色信息表格
                st.markdown("### 📊 色彩明细")
                color_data = []
                for i, rgb in enumerate(palette):
                    hex_c = rgb_to_hex(rgb)
                    color_data.append({
                        "序号": i+1,
                        "RGB": str(rgb),
                        "HEX": hex_c,
                        "色块": f"<div style='width:30px;height:30px;background:{hex_c};border-radius:4px;'></div>"
                    })
                st.markdown(
                    "<table style='border-collapse:collapse;width:100%;'>" +
                    "<tr style='background:#222;color:#eee;'><th style='padding:8px;border:1px solid #444;'>序号</th><th style='padding:8px;border:1px solid #444;'>RGB</th><th style='padding:8px;border:1px solid #444;'>HEX</th><th style='padding:8px;border:1px solid #444;'>色块</th></tr>" +
                    "".join([f"<tr style='background:#111;'><td style='padding:8px;border:1px solid #333;'>{d['序号']}</td><td style='padding:8px;border:1px solid #333;'>{d['RGB']}</td><td style='padding:8px;border:1px solid #333;'>{d['HEX']}</td><td style='padding:8px;border:1px solid #333;'>{d['色块']}</td></tr>" for d in color_data]) +
                    "</table>",
                    unsafe_allow_html=True
                )

                # AI 色彩分析
                st.markdown("### 🤖 AI 色彩分析")
                with st.spinner("🤖 AI 正在分析色彩运用..."):
                    image_b64 = image_to_base64(image, max_size=512)
                    prompt = f"""请对这张艺术作品的色彩运用进行专业分析。

请从以下角度分析（用简体中文，详细且专业）：

1. **主色调**：画面中占据主导地位的颜色及其情感表达
2. **色彩对比**：冷暖对比、明暗对比、互补色运用
3. **色彩和谐性**：色调是否统一，色彩过渡是否自然
4. **光影与色彩**：光源色、环境色、阴影色的处理
5. **色彩的象征意义**：不同颜色在作品中的文化与情感内涵
6. **技法层面**：画家/艺术家是如何运用色彩的（如印象派的光色、表现主义的情感色彩等）

另外，我从画面中提取了以下主色调（RGB格式）：
{str([rgb_to_hex(c) for c in palette])}

请结合这些实际数据进行专业分析。
"""
                    ai_color_analysis = analyze_image_with_vision(image_b64, prompt)

                st.markdown(ai_color_analysis)
                st.success("✅ 色彩分析完成！")

# ========== 版权信息 ==========
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#666;font-size:0.85rem;'>🎨 艺术分析助手 | Powered by AG2 + Multi-Agent AI | 支持文字 · 识图 · 色彩分析</p>",
    unsafe_allow_html=True
)
