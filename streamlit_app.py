import streamlit as st
import os
from dotenv import load_dotenv
import base64
from io import BytesIO
from PIL import Image
import colorsys

# 加载.env文件
load_dotenv()

# Page config
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

# 配置
API_KEY = os.getenv("OPENROUTER_API_KEY", "")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://api.siliconflow.cn/v1")

# 文本模型（用于文字分析）
TEXT_MODEL = os.getenv("AG2_DEFAULT_MODEL", "Qwen/Qwen2.5-7B-Instruct")

# 视觉模型（用于图片分析）- 必须是支持图像的VLM
VISION_MODEL = os.getenv("VISION_MODEL", "Qwen/Qwen3-VL-8B-Instruct")

# 如果视觉模型配置错误，给出提示
if VISION_MODEL == TEXT_MODEL:
    st.warning("⚠️ 视觉模型和文本模型相同，请确保 VISION_MODEL 设置为支持图像的模型（如 Qwen/Qwen3-VL-8B-Instruct）")

# 标题
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
st.markdown("### 基于 **AG2** 多智能体框架 | 输入艺术作品名称或上传图片开始分析")
st.markdown("---")

# 检查API配置
if not API_KEY:
    st.error("⚠️ 未配置API Key！请在 .env 文件中设置 OPENROUTER_API_KEY")
    st.stop()

# 功能选择
tab1, tab2 = st.tabs(["📝 文字分析", "🖼️ 图片分析"])

# ============ 文字分析标签页 ============
with tab1:
    col1, col2 = st.columns([3, 1])
    
    with col1:
        artwork = st.text_input(
            "请输入艺术作品名称", 
            placeholder="如：蒙娜丽莎、星空、向日葵、最后的晚餐",
            label_visibility="collapsed",
            key="text_input"
        )
    
    with col2:
        analyze_btn = st.button("🎨 开始分析", use_container_width=True, key="btn_text")
    
    # 示例按钮
    st.markdown("💡 **快速示例：**")
    examples = ["蒙娜丽莎", "星空", "向日葵", "格尔尼卡", "记忆的永恒"]
    cols = st.columns(len(examples))
    for i, ex in enumerate(examples):
        if cols[i].button(ex, key=f"ex_{i}"):
            artwork = ex
            analyze_btn = True
    
    # 文字分析逻辑
    if analyze_btn and artwork:
        with st.spinner(f"🎨 AI正在分析《{artwork}》，请稍候..."):
            try:
                from openai import OpenAI
                
                client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
                
                response = client.chat.completions.create(
                    model=TEXT_MODEL,
                    messages=[
                        {"role": "system", "content": """你是一位专业的艺术分析师，专门从事视觉艺术分析。
                        
请详细分析艺术作品，包括：
1. 构图与空间处理
2. 色彩运用与光影
3. 技法与风格特点  
4. 象征意义与主题
5. 历史背景与文化语境

请提供详细、具有教育意义的简体中文回复。使用优雅的Markdown格式。"""},
                        {"role": "user", "content": f"请详细分析这件艺术作品：{artwork}，提供至少5个关键见解。用中文回复。"}
                    ],
                    temperature=0.2,
                    max_tokens=4000
                )
                
                result = response.choices[0].message.content
                
                st.markdown("---")
                st.markdown(result)
                st.markdown("---")
                st.success("✅ 分析完成！")
                
            except Exception as e:
                st.error(f"❌ 分析出错: {str(e)}")

# ============ 图片分析标签页 ============
with tab2:
    st.markdown("#### 📤 上传图片开始分析")
    
    # 图片上传
    uploaded_file = st.file_uploader(
        "支持 JPG、PNG 格式",
        type=['jpg', 'jpeg', 'png'],
        help="上传艺术作品照片进行分析"
    )
    
    if uploaded_file is not None:
        # 显示上传的图片
        image = Image.open(uploaded_file)
        st.image(image, caption="上传的图片", use_column_width=True)
        
        # 色彩分析按钮
        if st.button("🎨 分析图片", key="btn_image"):
            with st.spinner("🎨 AI正在分析图片，请稍候..."):
                try:
                    from openai import OpenAI
                    
                    # 将图片转为base64
                    buffered = BytesIO()
                    image.save(buffered, format=image.format or "PNG")
                    img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
                    
                    # 构建多模态消息
                    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
                    
                    # 使用支持视觉的模型
                    response = client.chat.completions.create(
                        model=VISION_MODEL,
                        messages=[
                            {"role": "system", "content": """你是一位专业的艺术分析师，专门从事视觉艺术分析。
                            
请详细分析这张图片中的艺术作品，包括：
1. 画面构图与元素分析
2. 色彩运用与情感表达
3. 技法与风格特点
4. 象征意义与主题
5. 艺术价值评估

请提供详细、具有教育意义的简体中文回复。"""},
                            {"role": "user", "content": [
                                {"type": "text", "text": "请详细分析这张图片中的艺术作品，提供至少5个关键见解。用中文回复。"},
                                {"type": "image_url", "image_url": {"url": f"data:image/{image.format or 'png'};base64,{img_base64}"}}
                            ]}
                        ],
                        temperature=0.2,
                        max_tokens=4000
                    )
                    
                    result = response.choices[0].message.content
                    
                    st.markdown("---")
                    st.subheader("🎨 艺术分析结果")
                    st.markdown(result)
                    
                    # 色彩分析
                    st.markdown("---")
                    st.subheader("🎨 色彩分析")
                    
                    # 提取主色调
                    colors = extract_dominant_colors(image, 5)
                    
                    color_cols = st.columns(len(colors))
                    for i, (color, hex_color) in enumerate(colors):
                        with color_cols[i]:
                            st.color_picker(f"主色调 {i+1}", hex_color, disabled=True)
                            st.markdown(f"**{hex_color}**")
                            # 显示颜色名称
                            color_name = get_color_name(color)
                            st.caption(color_name)
                    
                    # 色彩情绪分析
                    color_mood = analyze_color_mood(colors)
                    st.markdown("---")
                    st.subheader("💫 色彩情绪")
                    st.markdown(color_mood)
                    
                    st.markdown("---")
                    st.success("✅ 分析完成！")
                    
                except Exception as e:
                    st.error(f"❌ 分析出错: {str(e)}")
                    # 如果是模型不支持视觉，提示用户
                    if "vision" in str(e).lower() or "image" in str(e).lower() or "VLM" in str(e).lower():
                        st.info("💡 当前模型可能不支持图片分析，请确保在 Render Dashboard 中设置了 VISION_MODEL=Qwen/Qwen3-VL-8B-Instruct")

# 版权信息
st.markdown("---")
st.markdown("<p style='text-align:center;color:#888;'>Powered by AG2 + 多模态大模型</p>", unsafe_allow_html=True)

# ============ 辅助函数 ============

def extract_dominant_colors(image, num_colors=5):
    """提取图片主色调"""
    # 缩小图片以加快处理速度
    img = image.copy()
    img.thumbnail((100, 100))
    
    # 转换为RGB
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # 获取像素
    pixels = list(img.getdata())
    
    # 简单聚类：按颜色分组
    from collections import Counter
    # 简化处理：采样像素
    sample = pixels[::10]  # 每10个像素取1个
    
    # 统计颜色
    color_counts = Counter(sample)
    most_common = color_counts.most_common(num_colors)
    
    colors = []
    for color, _ in most_common:
        # 转换为十六进制
        hex_color = '#{:02x}{:02x}{:02x}'.format(color[0], color[1], color[2])
        colors.append((color, hex_color))
    
    return colors

def get_color_name(rgb):
    """获取颜色名称"""
    r, g, b = rgb[0]/255, rgb[1]/255, rgb[2]/255
    
    # 简单判断
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    
    if max_val - min_val < 0.1:
        if max_val < 0.3:
            return "黑色/深色"
        elif max_val < 0.6:
            return "灰色"
        else:
            return "白色/浅色"
    
    # 判断色相
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    
    if s < 0.2:
        return "中性色"
    
    if h < 0.08 or h > 0.92:
        return "红色系"
    elif h < 0.17:
        return "橙色系"
    elif h < 0.25:
        return "黄色系"
    elif h < 0.42:
        return "绿色系"
    elif h < 0.58:
        return "蓝色系"
    elif h < 0.75:
        return "紫色系"
    elif h < 0.85:
        return "粉色系"
    else:
        return "红色系"

def analyze_color_mood(colors):
    """分析色彩情绪"""
    if not colors:
        return "无法分析"
    
    # 分析主色调
    primary = colors[0][0]
    r, g, b = primary[0]/255, primary[1]/255, primary[2]/255
    
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    
    # 分析情绪
    moods = []
    
    if v < 0.3:
        moods.append("深沉、神秘")
    elif v > 0.8:
        moods.append("明亮、轻快")
    
    if s < 0.3:
        moods.append("平和、宁静")
    elif s > 0.7:
        moods.append("强烈、热情")
    
    if h < 0.08 or h > 0.92:
        moods.append("充满活力、热情")
    elif h >= 0.08 and h < 0.17:
        moods.append("温暖、欢快")
    elif h >= 0.17 and h < 0.42:
        moods.append("自然、生机")
    elif h >= 0.42 and h < 0.67:
        moods.append("冷静、专业")
    elif h >= 0.67 and h < 0.85:
        moods.append("浪漫、高贵")
    
    # 整体色彩丰富度
    if len(colors) >= 4:
        moods.append("色彩丰富")
    elif len(colors) >= 2:
        moods.append("色彩协调")
    
    return "、".join(moods[:4]) if moods else "色彩平衡"