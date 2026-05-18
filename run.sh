#!/bin/bash
echo "========================================"
echo "  艺术分析助手 - 一键启动"
echo "========================================"
echo ""

cd "$(dirname "$0")"

echo "[1/3] 检查Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python，请先安装Python 3.10+"
    exit 1
fi

echo "[2/3] 安装依赖..."
pip3 install -q -r requirements.txt 2>/dev/null

echo "[3/3] 启动服务..."
echo ""
echo "🎨 服务启动中，请访问: http://localhost:8501"
echo ""
echo "按 Ctrl+C 可以停止服务"
echo ""

streamlit run streamlit_app.py