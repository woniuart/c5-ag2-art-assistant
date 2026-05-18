import streamlit as st
import os
import base64
import io
from dotenv import load_dotenv
from PIL import Image
import colorthief
import json

# 加载.env文件
load_dotenv()

# ========== 配置 ==========
API_KEY = os.getenv("OPENROUTER_API_KEY", "")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://api.siliconflow.cn/v1")
MODEL = os.getenv("AG2_DEFAULT_MODEL", "MiniMaxAI/MiniMax-M2.5")
VISION_MODEL = os.getenv("VISION_MODEL", "Qwen/Qwen2-VL-7B-Instruct")
VISION_BASE_URL = os.getenv("VISION_BASE_URL", BASE_URL)

# 多模型配置
VISION_MODEL_OPTIONS_STR = os.getenv("VISION_MODEL_OPTIONS", "")
VISION_MODEL_OPTIONS = [m.strip() for m in VISION_MODEL_OPTIONS_STR.split(",") if m.strip()] if VISION_MODEL_OPTIONS_STR else []

# 技能开关
ENABLE_COMPOSITION_ANALYSIS = os.getenv("ENABLE_COMPOSITION_ANALYSIS", "true").lower() == "true"
ENABLE_STYLE_ANALYSIS = os.getenv("ENABLE_STYLE_ANALYSIS", "true").lower() == "true"
ENABLE_HISTORICAL_CONTEXT = os.getenv("ENABLE_HISTORICAL_CONTEXT", "true").lower() == "true"
ENABLE_EMOTION_ANALYSIS = os.getenv("ENABLE_EMOTION_ANALYSIS", "true").lower() == "true"
ENABLE_TECHNIQUE_ANALYSIS = os.getenv("ENABLE_TECHNIQUE_ANALYSIS", "true").lower() == "true"
ENABLE_COLOR_ANALYSIS = os.getenv("ENABLE_COLOR_ANALYSIS", "true").lower() == "true"

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
st.markdown("### 基于 **多智能体 AI** | 支持文字分析 · 图片识图 · 色彩分析 · 多模型")
st.markdown("---")

# ========== 检查API配置 ==========
if not API_KEY:
    st.error("⚠️ 未配置 API Key！请在 .env 文件中设置 OPENROUTER_API_KEY")
    st.info("当前使用 SiliconFlow API，请在 .env 中填写你的 API Key")
    st.stop()

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
        ct = colorthief.ColorThief(image)
        palette = ct.get_palette(color_count=num_colors)
        dominant = ct.get_color(quality=1)
        return palette, dominant
    except Exception:
        # fallback：使用 PIL 简单采样
        img = image.copy()
        img.thumbnail((100, 100))
        pixels = list(img.getdata())
        from collections import Counter
        counter = Counter(pixels)
        palette = [c for c, _ in counter.most_common(num_colors)]
        dominant = palette[0] if palette else (0, 0, 0)
        return palette, dominant


def rgb_to_hex(rgb):
    """rgb 转 hex"""
    return "#{:02x}{:02x}{:02x}".format(
        max(0, min(255, rgb[0])),
        max(0, min(255, rgb[1])),
        max(0, min(255, rgb[2]))
    )


def analyze_image_with_vision(image_b64: str, prompt: str, model: str = None, base_url: str = None) -> str:
    """调用视觉大模型分析图片"""
    try:
        from openai import OpenAI
        
        use_model = model or VISION_MODEL
        use_base_url = base_url or VISION_BASE_URL
        
        client = OpenAI(api_key=API_KEY, base_url=use_base_url)
        
        messages = [
            {"role": "system", "content": "你是一位专业的艺术史学者和视觉艺术分析师，擅长从图像中分析艺术作品。请用简体中文详细回复，格式清晰，适合教学使用。"},
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
            ]}
        ]
        
        response = client.chat.completions.create(
            model=use_model,
            messages=messages,
            max_tokens=2000,
            temperature=0.3,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"视觉分析出错: {str(e)}"


def analyze_text(artwork: str, model: str = None) -> str:
    """文字输入分析（原有功能）"""
    try:
        from openai import OpenAI
        
        use_model = model or MODEL
        client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
        
        response = client.chat.completions.create(
            model=use_model,
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


# ========== 侧边栏：模型和技能配置 ==========
with st.sidebar:
    st.header("⚙️ 设置")
    
    # 模型选择
    st.markdown("#### 🤖 选择视觉模型")
    
    # 默认模型
    model_options = [VISION_MODEL]
    
    # 添加配置的多个模型
    if VISION_MODEL_OPTIONS:
        model_options.extend([m for m in VISION_MODEL_OPTIONS if m not in model_options])
    
    # 添加常用模型（如果没配置）
    common_models = [
        "Qwen/Qwen2-VL-7B-Instruct",
        "Qwen/Qwen2-VL-72B-Instruct",
        "google/gemini-2.0-flash-001",
        "anthropic/claude-3.5-sonnet",
        "openai/gpt-4o"
    ]
    for m in common_models:
        if m not in model_options:
            model_options.append(m)
    
    selected_vision_model = st.selectbox(
        "视觉分析模型",
        model_options,
        index=0,
        key="vision_model_select"
    )
    
    st.markdown("---")
    
    # 分析技能开关
    st.markdown("#### 🎯 分析技能")
    
    enable_composition = st.checkbox("构图分析", value=ENABLE_COMPOSITION_ANALYSIS, key="skill_composition")
    enable_style = st.checkbox("风格分析", value=ENABLE_STYLE_ANALYSIS, key="skill_style")
    enable_historical = st.checkbox("历史背景", value=ENABLE_HISTORICAL_CONTEXT, key="skill_historical")
    enable_emotion = st.checkbox("情感分析", value=ENABLE_EMOTION_ANALYSIS, key="skill_emotion")
    enable_technique = st.checkbox("技法分析", value=ENABLE_TECHNIQUE_ANALYSIS, key="skill_technique")
    enable_color = st.checkbox("色彩分析", value=ENABLE_COLOR_ANALYSIS, key="skill_color")
    
    st.markdown("---")
    
    # 模型信息
    st.markdown("**当前文本模型**")
    st.code(MODEL)
    st.markdown("**当前视觉模型**")
    st.code(selected_vision_model)

# ========== 主界面：统一输入 ==========

st.markdown("## 📝 艺术分析")

# 输入方式选择
input_mode = st.radio(
    "选择输入方式",
    ["📝 输入作品名称", "📷 上传图片分析", "📝+📷 同时提供名称和图片"],
    index=0,
    horizontal=True
)

st.markdown("---")

# 根据选择的方式显示输入界面
if input_mode == "📝 输入作品名称":
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
            result = analyze_text(artwork, model=MODEL)
        st.markdown("---")
        st.markdown(result)
        st.markdown("---")
        st.success("✅ 分析完成！")

elif input_mode == "📷 上传图片分析":
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
            with st.spinner(f"🤖 视觉AI（{selected_vision_model}）正在识别并分析图片，请稍候（约30秒）..."):
                image_b64 = image_to_base64(image, max_size=512)
                
                # 构建分析提示词
                prompt = """请识别并分析这张艺术作品图片。\n\n请按以下结构回复（用简体中文）：\n\n## 📋 作品识别"""
                prompt += """
- 作品名称（如能识别）
- 艺术家
- 创作年代（如能判断）
- 艺术流派

## 🔬 艺术分析"""
                
                if enable_composition:
                    prompt += "\n1. **构图分析**：画面布局、视觉中心、空间处理"
                
                if enable_style:
                    prompt += "\n2. **风格分析**：艺术流派、风格特点、技法特征"
                
                if enable_technique:
                    prompt += "\n3. **技法分析**：笔触、材质、表现手法"
                
                if enable_color:
                    prompt += "\n4. **色彩分析**：主色调、色彩对比、情感表达"
                
                if enable_emotion:
                    prompt += "\n5. **情感分析**：作品传达的情绪、氛围、观者感受"
                
                if enable_historical:
                    prompt += "\n6. **历史背景**：创作时代、社会语境、文化意义"
                
                prompt += "\n\n## 💬 教学建议\n- 2-3个适合课堂讨论的问题\n- 延伸学习资源推荐\n\n请详细、专业、具有教育意义。"
                
                result = analyze_image_with_vision(image_b64, prompt, model=selected_vision_model)
            
            st.markdown("---")
            st.markdown(result)
            st.markdown("---")
            st.success("✅ 识图分析完成！")

elif input_mode == "📝+📷 同时提供名称和图片":
    st.markdown("提供作品名称和图片，AI 将结合两者进行更深入的分析。")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        artwork_name = st.text_input(
            "作品名称（可选）",
            placeholder="如：星空、蒙娜丽莎",
            key="combined_name"
        )
    
    with col2:
        uploaded_file = st.file_uploader(
            "上传作品图片",
            type=["jpg", "jpeg", "png", "webp"],
            key="combined_uploader"
        )
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="上传的图片", width=300)
    
    analyze_combined_btn = st.button("🎨 开始综合分析", use_container_width=True, key="combined_btn")
    
    if analyze_combined_btn:
        if not artwork_name and uploaded_file is None:
            st.error("⚠️ 请提供作品名称或上传图片（至少一项）")
        else:
            with st.spinner(f"🤖 AI（{selected_vision_model}）正在进行综合分析，请稍候..."):
                if uploaded_file is not None:
                    image_b64 = image_to_base64(image, max_size=512)
                
                if artwork_name and uploaded_file is not None:
                    # 两者都有：结合分析
                    prompt = f"""用户提供了作品名称：《{artwork_name}》。请结合这幅图片和作品名称进行详细分析。\n\n请按以下结构回复（用简体中文）：\n\n## 📋 作品信息\n- 作品名称：《{artwork_name}》\n- 确认艺术家和创作年代\n- 艺术流派\n\n## 🔬 艺术分析"""
                    
                    if enable_composition:
                        prompt += "\n1. **构图分析**：画面布局、视觉中心、空间处理"
                    
                    if enable_style:
                        prompt += "\n2. **风格分析**：艺术流派、风格特点、技法特征"
                    
                    if enable_technique:
                        prompt += "\n3. **技法分析**：笔触、材质、表现手法"
                    
                    if enable_color:
                        prompt += "\n4. **色彩分析**：主色调、色彩对比、情感表达"
                    
                    if enable_emotion:
                        prompt += "\n5. **情感分析**：作品传达的情绪、氛围、观者感受"
                    
                    if enable_historical:
                        prompt += "\n6. **历史背景**：创作时代、社会语境、文化意义"
                    
                    prompt += "\n\n## 💬 教学建议\n- 2-3个适合课堂讨论的问题\n- 延伸学习资源推荐\n\n请详细、专业、具有教育意义。"
                    
                    try:
                        from openai import OpenAI
                        client = OpenAI(api_key=API_KEY, base_url=VISION_BASE_URL)
                        
                        messages = [
                            {"role": "system", "content": "你是一位专业的艺术史学者和视觉艺术分析师。"},
                            {"role": "user", "content": [
                                {"type": "text", "text": prompt},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
                            ]}
                        ]
                        
                        response = client.chat.completions.create(
                            model=selected_vision_model,
                            messages=messages,
                            max_tokens=2000,
                            temperature=0.3,
                        )
                        result = response.choices[0].message.content
                    except Exception as e:
                        result = f"分析出错: {str(e)}"
                elif artwork_name:
                    # 只有文字
                    result = analyze_text(artwork_name, model=MODEL)
                else:
                    # 只有图片
                    prompt = """请识别并分析这张艺术作品图片。\n\n请按以下结构回复（用简体中文）：\n\n## 📋 作品识别\n- 作品名称（如能识别）\n- 艺术家\n- 创作年代（如能判断）\n- 艺术流派\n\n## 🔬 艺术分析"""
                    
                    if enable_composition:
                        prompt += "\n1. **构图分析**"
                    
                    if enable_style:
                        prompt += "\n2. **风格分析**"
                    
                    if enable_technique:
                        prompt += "\n3. **技法分析**"
                    
                    if enable_color:
                        prompt += "\n4. **色彩分析**"
                    
                    if enable_emotion:
                        prompt += "\n5. **情感分析**"
                    
                    if enable_historical:
                        prompt += "\n6. **历史背景**"
                    
                    prompt += "\n\n请详细、专业、具有教育意义。"
                    
                    result = analyze_image_with_vision(image_b64, prompt, model=selected_vision_model)
            
            st.markdown("---")
            st.markdown(result)
            st.markdown("---")
            st.success("✅ 综合分析完成！")

# ========== 高级功能：色彩分析（侧边栏） ==========
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🎨 专业色彩分析")
    st.markdown("上传图片进行专业的色彩提取与AI分析")
    
    color_file = st.file_uploader(
        "选择图片",
        type=["jpg", "jpeg", "png", "webp"],
        key="sidebar_color_uploader"
    )
    
    if color_file is not None:
        color_image = Image.open(color_file).convert("RGB")
        num_colors = st.slider("提取主色数量", min_value=3, max_value=10, value=6, key="color_slider")
        
        if st.button("🎨 开始色彩分析", key="sidebar_color_btn"):
            with st.spinner("🎨 正在提取色彩并分析..."):
                # 提取主色调
                palette, dominant = extract_colors(color_image, num_colors)
                
                # 显示色彩面板
                st.markdown("#### 🎨 主色调提取")
                color_html = "<div style='display:flex; gap:8px; flex-wrap:wrap; margin:10px 0;'>"
                for rgb in palette:
                    hex_c = rgb_to_hex(rgb)
                    color_html += f"<div style='width:60px;height:60px;background:{hex_c};border-radius:8px;border:1px solid #555;' title='{hex_c} RGB{rgb}'></div>"
                color_html += "</div>"
                st.markdown(color_html, unsafe_allow_html=True)
                
                # 主色信息表格
                st.markdown("#### 📊 色彩明细")
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
                st.markdown("#### 🤖 AI 色彩分析")
                with st.spinner("🤖 AI 正在分析色彩运用..."):
                    image_b64 = image_to_base64(color_image, max_size=512)
                    prompt = f"""请对这张艺术作品的色彩运用进行专业分析。\n\n请从以下角度分析（用简体中文，详细且专业）：\n\n1. **主色调**：画面中占据主导地位的颜色及其情感表达\n2. **色彩对比**：冷暖对比、明暗对比、互补色运用\n3. **色彩和谐性**：色调是否统一，色彩过渡是否自然\n4. **光影与色彩**：光源色、环境色、阴影色的处理\n5. **色彩的象征意义**：不同颜色在作品中的文化与情感内涵\n6. **技法层面**：画家/艺术家是如何运用色彩的（如印象派的光色、表现主义的情感色彩等）\n\n另外，我从画面中提取了以下主色调（RGB格式）：\n{str([rgb_to_hex(c) for c in palette])}\n\n请结合这些实际数据进行专业分析。"""
                    ai_color_analysis = analyze_image_with_vision(image_b64, prompt, model=selected_vision_model)
                
                st.markdown(ai_color_analysis)
                st.success("✅ 色彩分析完成！")

# ========== 版权信息 ==========
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#666;font-size:0.85rem;'>🎨 艺术分析助手 | Powered by AG2 + Multi-Agent AI | 支持文字 · 识图 · 色彩分析 · 多模型</p>",
    unsafe_allow_html=True
)
