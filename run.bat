@echo off
echo ========================================
echo   艺术分析助手 - 一键启动
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] 检查Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python，请先安装Python 3.10+
    pause
    exit /b 1
)

echo [2/3] 安装依赖...
pip install -q -r requirements.txt 2>nul

echo [3/3] 启动服务...
echo.
echo 🎨 服务启动中，请访问: http://localhost:8501
echo.
echo 按 Ctrl+C 可以停止服务
echo.

streamlit run streamlit_app.py

pause