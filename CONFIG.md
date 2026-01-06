# 环境配置指南

## 快速开始

### 1. 配置 API Key

打开项目根目录的 `.env` 文件，将你的 API Key 填入：

```bash
# 使用阿里云通义千问（推荐）
OPENAI_API_KEY=sk-你的真实API-Key
OPENAI_API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1
OPENAI_MODEL=qwen-plus
```

### 2. 获取 API Key

#### 阿里云 DashScope (通义千问) - 推荐

1. 访问：https://dashscope.console.aliyun.com/apiKey
2. 登录阿里云账号
3. 创建 API Key
4. 复制 API Key 到 `.env` 文件

**优势：**
- 国内访问速度快
- 价格便宜
- 支持多种模型（qwen-plus, qwen-turbo, qwen-max）

#### OpenAI

1. 访问：https://platform.openai.com/api-keys
2. 登录 OpenAI 账号
3. 创建 API Key
4. 修改 `.env` 文件：

```bash
OPENAI_API_KEY=sk-你的OpenAI-Key
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
```

#### DeepSeek

1. 访问：https://platform.deepseek.com/
2. 登录并创建 API Key
3. 修改 `.env` 文件：

```bash
OPENAI_API_KEY=sk-你的DeepSeek-Key
OPENAI_API_BASE=https://api.deepseek.com/v1
OPENAI_MODEL=deepseek-chat
```

## 验证配置

运行环境检查脚本：

```bash
cd 01-plan-execute
python check_env.py
```

应该看到：

```
============================================================
🔍 检查环境配置
============================================================
✅ OPENAI_API_KEY: sk-xxxxxx...xxxx
✅ OPENAI_API_BASE: https://dashscope.aliyuncs.com/compatible-mode/v1
✅ OPENAI_MODEL: qwen-plus
------------------------------------------------------------
✅ .env 文件存在
============================================================

✅ 环境配置检查通过！

🚀 可以启动服务了！运行: python start.py
```

## 常见问题

### 1. API Key 无效

**错误信息：**
```
httpcore.ConnectError: [Errno 11001] getaddrinfo failed
```

**解决方法：**
- 检查 `.env` 文件是否存在
- 确认 API Key 已正确填写
- 确保 API Key 没有多余的空格或引号

### 2. 网络连接失败

**错误信息：**
```
ConnectError: connection error
```

**解决方法：**
- 检查网络连接
- 尝试使用阿里云 DashScope（国内访问更快）
- 如果使用代理，确保代理配置正确

### 3. 权限不足

**错误信息：**
```
Error: 401 Unauthorized
```

**解决方法：**
- 确认 API Key 有效
- 检查账户余额
- 验证 API Key 权限

### 4. 模型不存在

**错误信息：**
```
Error: Model not found
```

**解决方法：**
- 检查模型名称拼写
- 确认该模型在你的账户中可用
- 查看服务商文档了解可用模型列表

## 支持的模型

### 阿里云 DashScope
- `qwen-plus` - 通用模型，推荐
- `qwen-turbo` - 速度快
- `qwen-max` - 能力最强
- `qwen-long` - 长文本

### OpenAI
- `gpt-4o-mini` - 推荐
- `gpt-4o` - 最强
- `gpt-3.5-turbo` - 经济

### DeepSeek
- `deepseek-chat` - 通用对话
- `deepseek-coder` - 代码专用

## 环境变量说明

| 变量名 | 必需 | 说明 | 示例 |
|--------|------|------|------|
| OPENAI_API_KEY | ✅ | API 密钥 | sk-xxxxxx |
| OPENAI_API_BASE | ✅ | API 地址 | https://api.openai.com/v1 |
| OPENAI_MODEL | ✅ | 模型名称 | gpt-4o-mini |

## 安全提示

⚠️ **重要：**
- 不要将 `.env` 文件提交到 Git
- 不要在公开代码中暴露 API Key
- 定期更换 API Key
- 为 API Key 设置使用限额

## 下一步

配置完成后，启动服务：

```bash
python start.py
```

服务启动后，访问 http://localhost:8000/docs 测试 API
