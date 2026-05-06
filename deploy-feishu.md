# 🎨 飞书智能体部署指南

本文档说明如何将艺术分析助手部署为飞书机器人/智能体。

---

## 方式一：飞书自定义机器人（最简单，推荐）

### 步骤1：创建飞书机器人

1. 打开飞书电脑版，进入任意群聊
2. 点击右上角「设置」→「群设置」→「添加机器人」
3. 选择「自定义机器人」
4. 给机器人起名（如「艺术分析助手」）
5. 复制机器人 Webhook 地址（格式：`https://open.feishu.cn/open-apis/bot/v2/hook/xxx`）

### 步骤2：运行服务

```bash
# 安装依赖
pip install -r requirements.txt

# 启动API服务（本地端口8000）
python3 api.py
```

### 步骤3：配置内网穿透

飞书需要能访问到你的服务，使用 ngrok 免费穿透：

```bash
# 方法1: ngrok（需要注册）
ngrok http 8000

# 方法2: natapp（国内推荐）
# https://natapp.cn 下载客户端，运行：
# natapp -authtoken=你的token -port=8000

# 方法3: cloudflared（国外）
cloudflared tunnel --url http://localhost:8000
```

复制得到的公网URL，例如：`https://xxx.ngrok.io`

### 步骤4：配置机器人消息推送

飞书自定义机器人的 Webhook 是被动接收消息，若需要主动回复，需要：

**方案A：使用飞书开放平台应用（推荐）**

1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 创建企业应用 → 开通权限：`im:message:send_as_bot`
3. 获取 App ID 和 App Secret
4. 调用获取 tenant_access_token 接口
5. 使用 imchative/RoBotService/api 回复消息

**方案B：使用现有飞书智能体（如果有）**

如果有飞书智能体权限，可以在飞书智能体后台配置 Webhook。

---

## 方式二：飞书智能体（企业功能）

如果你的企业已开通飞书智能体：

1. 登录飞书智能体管理后台
2. 创建新智能体「艺术分析助手」
3. 配置大模型为你的后端API
4. 在提示词中说明调用 `/analyze` 接口
5. 发布智能体到企业应用市场

---

## 快速测试

### 测试API服务

```bash
# 启动服务后，测试分析接口
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"artwork": "《蒙娜丽莎》by Leonardo da Vinci"}'
```

响应示例：
```json
{
  "success": true,
  "result": "《蒙娜丽莎》深度分析\n\n## 1. 构图与空间处理\n\n蒙娜丽莎的构图体现了...",
  "artwork": "《蒙娜丽莎》by Leonardo da Vinci"
}
```

### 测试飞书Webhook（模拟）

```bash
# 模拟飞书发送的消息（测试用）
curl -X POST https://你的公网地址/feishu/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "event": {
      "message": {
        "message_type": "text",
        "text": {"content": "分析一下《星空》by梵高"}
      }
    }
  }'
```

---

## 常见问题

### Q1: 飞书机器人发消息没反应

1. 检查服务是否运行：`curl http://localhost:8000/health`
2. 检查内网穿透是否正常：`curl https://你的ngrok地址/health`
3. 检查Webhook URL是否正确

### Q2: 提示API Key错误

确保 `.env` 文件中有正确的 API Key：
```
OPENROUTER_API_KEY=your_key_here
```

### Q3: 响应太慢

1. 首次调用需要加载模型，可能需要10-30秒
2. 检查网络到 SiliconFlow/OpenRouter 的连接

### Q4: 想让更多人在手机上用

**方案A**：将服务部署到云服务器（阿里云/腾讯云/火山引擎）
- 购买云服务器，安装Python环境
- 使用 Docker 部署
- 直接使用公网IP，无需内网穿透

**方案B**：使用飞书企业应用
- 申请企业应用资质
- 发布到企业应用市场
- 员工可在飞书APP内直接使用

---

## 生产环境部署（推荐）

如果准备正式使用，推荐部署到云服务器：

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY api.py .
COPY .env .

EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# 构建并运行
docker build -t art-assistant .
docker run -d -p 8000:8000 --env-file .env art-assistant
```

---

## 文件结构

部署后的项目结构：

```
c5-ag2-art-assistant/
├── api.py              # FastAPI Web服务（新增）
├── main.py             # 原始CLI程序（保留）
├── requirements.txt    # Python依赖
├── .env                # 环境变量（API Key）
├── README.md           # 项目说明
├── deploy-feishu.md    # 本文件
└── Dockerfile          # Docker部署文件（可选）
```

---

## 下一步

1. 运行 `python3 api.py` 本地测试
2. 配置内网穿透获取公网URL
3. 在飞书群添加自定义机器人
4. 开始使用！

有任何问题随时问我。