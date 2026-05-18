# Dockerfile for Art Analysis API
# 构建: docker build -t art-assistant .
# 运行: docker run -d -p 8000:8000 --env-file .env art-assistant

FROM python:3.10-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY api.py .
COPY main.py .

# 复制环境变量文件（需要预先配置）
COPY .env .env

# 暴露端口
EXPOSE 8000

# 启动服务
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]