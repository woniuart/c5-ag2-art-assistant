import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

# Page config
st.set_page_config(
    page_title="艺术分析助手",
    page_title="🎨 艺术分析助手",
    layout="wide"
)

# 配置
API_KEY = os.getenv("OPENROUTER_API_KEY", "")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://api.siliconflow.cn/v1")
MODEL = os.getenv("AG2_DEFAULT_MODEL", "MiniMaxAI/MiniMax-M2.5")

from openai import OpenAI

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# Title
st.title("🎨 艺术分析助手")
st.markdown("基于 **AG2** 多智能体框架 | 输入艺术作品名称开始分析")

# Input
artwork = st.text_input("请输入艺术作品名称", placeholder="如：蒙娜丽莎、星空、向日葵")

if st.button("开始分析"):
    if not artwork:
        st.warning("请输入作品名称")
    else:
        with st.spinner("🎨 AI正在分析中..."):
            try:
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {"role": "system", "content": "你是一位专业的艺术分析师，专门从事视觉艺术分析。请详细分析艺术作品，包括：构图、色彩、技法、象征意义、历史背景。提供详细、具有教育意义的简体中文回复。"},
                        {"role": "user", "content": f"请详细分析这件艺术作品：{artwork}，提供至少5个关键见解"}
                    ],
                    temperature=0.2,
                    max_tokens=4000
                )
                result = response.choices[0].message.content
                st.markdown(result)
            except Exception as e:
                st.error(f"分析出错: {str(e)}")

# Examples
st.markdown("---")
st.markdown("💡 **建议作品**：蒙娜丽莎、星空、向日葵、最后的晚餐、记忆的永恒、格尔尼卡")
