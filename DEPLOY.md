# 🎨 艺术分析助手 - 云端部署详细教程

## 一、注册账号

### 1. 打开Render官网
在浏览器中打开：**https://render.com**

### 2. 点击 Sign Up 注册
- 可以使用 GitHub 账号直接登录（推荐）
- 点击 "Sign in with GitHub"

### 3. 授权 GitHub
- 如果弹出授权页面，点击 "Authorize"

---

## 二、部署应用

### 1. 使用一键部署链接
直接打开以下链接：
```
https://render.com/deploy?repo=https://github.com/woniuart/c5-ag2-art-assistant
```

### 2. 选择部署方式
页面打开后，你会看到：
- **Owner**: 选择你的GitHub账号
- **Name**: 可以改成 `art-assistant` 或者其他名字
- **Branch**: 保持 `main`
- **Build Command**: 保持 `pip install -r requirements.txt`
- **Start Command**: 保持 `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0`

### 3. 选择付费计划
- **Free** 是免费的，选择它
- 点击下方绿色的 **Create Web Service** 按钮

---

## 三、配置环境变量

### 1. 进入设置页面
部署开始后，点击左侧菜单的 **Environment**

### 2. 添加变量
在 Environment Variables 区域，依次添加：

| 变量名 | 值 |
|--------|-----|
| OPENROUTER_API_KEY | sk-mdoklwrqimsbvjnruqrsdxmzoaycpekndmyvqgyymfqwooqa |
| OPENROUTER_BASE_URL | https://api.siliconflow.cn/v1 |
| AG2_DEFAULT_MODEL | MiniMaxAI/MiniMax-M2.5 |

### 3. 保存
- 添加完后，滚动到页面底部
- 点击 **Save Changes**
- 服务会自动重启

---

## 四、等待部署完成

### 1. 查看部署状态
- 页面会显示部署进度
- 等待看到绿色的 **Live** 标志

### 2. 获取公网链接
- 部署成功后，页面顶部会显示你的链接
- 格式类似：`https://art-assistant.onrender.com`
- 点击链接即可访问

---

## 五、使用方法

### 1. 打开应用
在浏览器中打开刚才获得的链接

### 2. 分析艺术作品
- 在输入框中输入作品名称，如：`蒙娜丽莎`、`星空`、`向日葵`
- 点击 **开始分析** 按钮
- 等待几秒钟，AI会返回分析结果

### 3. 查看结果
分析结果会显示在下方，包括：
- 构图分析
- 色彩运用
- 技法特点
- 象征意义
- 历史背景

---

## 六、常见问题

### Q: 部署失败了怎么办？
A: 查看部署日志，通常是缺少环境变量。确保上面三个环境变量都正确添加。

### Q: 用不了怎么办？
A: 检查环境变量是否保存成功，可以删除服务重新部署。

### Q: 链接打不开？
A: 免费服务有休眠机制，如果长时间不访问会休眠。访问一次就会自动唤醒。

---

## 七、原理解释

这个应用使用：
- **Streamlit**: 创建网页界面
- **SiliconFlow API**: 提供AI分析能力（免费额度）
- **MiniMax M2.5**: 分析用的AI模型

你不需要任何编程基础，只需要按照上面的步骤操作即可！

---

有任何问题随时问我！