import streamlit as st
import os
from dotenv import load_dotenv

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
MODEL = os.getenv("AG2_DEFAULT_MODEL", "MiniMaxAI/MiniMax-M2.5")

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
st.markdown("### 基于 **AG2** 多智能体框架 | 输入艺术作品名称开始分析")
st.markdown("---")

# 检查API配置
if not API_KEY:
    st.error("⚠️ 未配置API Key！请在 .env 文件中设置 OPENROUTER_API_KEY")
    st.stop()

# 输入区域
col1, col2 = st.columns([3, 1])

with col1:
    artwork = st.text_input(
        "请输入艺术作品名称", 
        placeholder="如：蒙娜丽莎、星空、向日葵、最后的晚餐",
        label_visibility="collapsed"
    )

with col2:
    analyze_btn = st.button("🎨 开始分析", use_container_width=True)

# 示例按钮
st.markdown("💡 **快速示例：**")
examples = ["蒙娜丽莎", "星空", "向日葵", "格尔尼卡", "记忆的永恒"]
cols = st.columns(len(examples))
for i, ex in enumerate(examples):
    if cols[i].button(ex, key=f"ex_{i}"):
        artwork = ex
        analyze_btn = True

# 分析逻辑
if analyze_btn and artwork:
    with st.spinner(f"🎨 AI正在分析《{artwork}》，请稍候..."):
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

# 版权信息
st.markdown("---")
st.markdown("<p style='text-align:center;color:#888;'>Powered by AG2 + MiniMax M2.5</p>", unsafe_allow_html=True)