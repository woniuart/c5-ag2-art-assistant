# 🎨 Art Analysis Assistant | 艺术分析助手

[![AG2 Beta](https://img.shields.io/badge/Framework-AG2%20Beta-blue)](https://docs.ag2.ai/)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green)](https://www.python.org/)

基于 AG2 (AutoGen) 框架的多智能体艺术分析系统

## 🚀 一键部署

### 方式1: Render (推荐，免费)
点击链接部署：
https://render.com/deploy?repo=https://github.com/woniuart/c5-ag2-art-assistant

部署后在Settings中添加环境变量：
- `OPENROUTER_API_KEY` = `sk-mdoklwrqimsbvjnruqrsdxmzoaycpekndmyvqgyymfqwooqa`
- `OPENROUTER_BASE_URL` = `https://api.siliconflow.cn/v1`
- `AG2_DEFAULT_MODEL` = `MiniMaxAI/MiniMax-M2.5`

### 方式2: 本地运行
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## 💡 使用方法

1. 在输入框中输入艺术作品名称（如：蒙娜丽莎、星空）
2. 点击"开始分析"
3. AI会自动分析作品并返回详细的艺术分析报告

## 📁 项目结构

- `streamlit_app.py` - Streamlit Web界面版本
- `api.py` - FastAPI后端版本
- `main.py` - 终端版本
- `requirements.txt` - Python依赖

## ⚠️ 注意

本项目使用SiliconFlow的免费API，有速率限制。如需大规模使用，请配置自己的API Key。

---
**Built with ❤️ using AG2 Beta & Streamlit**
