# LangAgent 学习实验室

这是一个从零开始的 LangChain/LangGraph/LLM Agent 学习空间。

## 📚 学习路径

### 01-plan-execute ✅
使用 LangGraph 实现经典的 Plan-Execute 模式
- 使用 LLM 生成执行计划
- 执行计划步骤
- 支持流式和非流式 API 接口
- **[查看项目](./01-plan-execute/README.md) | [快速开始](./01-plan-execute/QUICKSTART.md)**

### 02-multi-agent (待完成)
多 Agent 协作模式

### 03-rag-agent (待完成)
RAG + Agent 结合

### 04-tools-agent (待完成)
Agent 工具调用

### 05-memory-agent (待完成)
Agent 记忆管理

### 06-langgraph-advanced (待完成)
LangGraph 高级特性

## 🚀 快速开始

### 1. 安装依赖

```bash
# 使用国内镜像加速（推荐）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 安装第一个项目的依赖
pip install -r 01-plan-execute/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 2. 配置 API Key

**⚠️ 重要：必须先配置 API Key 才能运行**

```bash
# 复制配置文件
cp .env.example .env

# 编辑 .env 文件，填入你的 API Key
# 推荐使用阿里云通义千问（国内访问快）
```

**[详细配置指南](./CONFIG.md)** | **[安装指南](./01-plan-execute/INSTALL.md)**

### 3. 验证配置

```bash
cd 01-plan-execute
python check_env.py
```

### 4. 启动服务

```bash
python start.py
```

服务将在 http://localhost:8000 启动

### 5. 测试 API

```bash
# 访问 API 文档
# http://localhost:8000/docs

# 或运行测试脚本
python test_api.py
```

## 📖 文档

- [环境配置详解](./CONFIG.md) - API Key 获取和配置
- [项目 01 - 安装指南](./01-plan-execute/INSTALL.md) - 详细安装步骤
- [项目 01 - 快速开始](./01-plan-execute/QUICKSTART.md) - 5 分钟上手
- [项目 01 - 日志说明](./01-plan-execute/LOGGING.md) - 查看运行日志

## 🔧 技术栈

- **LangGraph** - Agent 工作流编排
- **LangChain** - LLM 应用框架
- **FastAPI** - 高性能 API 框架
- **OpenAI API** - LLM 接口（兼容多种服务）

## 💡 支持的 LLM 服务

- ✅ 阿里云 DashScope (通义千问) - **推荐国内用户**
- ✅ OpenAI (GPT-4, GPT-3.5)
- ✅ DeepSeek
- ✅ 其他兼容 OpenAI 的 API

## 📁 项目结构

```
LangAgent-Labs/
├── .env                  # 环境变量配置（需要创建）
├── .env.example          # 配置示例
├── CONFIG.md             # 环境配置指南
├── requirements.txt      # 依赖列表
│
└── 01-plan-execute/      # 第一个实战项目
    ├── src/              # 源代码
    ├── start.py          # 启动脚本
    ├── check_env.py      # 环境检查
    ├── test_api.py       # 测试脚本
    ├── README.md         # 项目说明
    ├── QUICKSTART.md     # 快速开始
    └── INSTALL.md        # 安装指南
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可

MIT License

## ❓ 常见问题

### Q: 如何获取 API Key？

**A:** 查看 [环境配置指南](./CONFIG.md)，支持多种服务：
- 阿里云 DashScope：https://dashscope.console.aliyun.com/apiKey
- OpenAI：https://platform.openai.com/api-keys
- DeepSeek：https://platform.deepseek.com/

### Q: 推荐使用哪个 LLM 服务？

**A:**
- 国内用户：**阿里云通义千问**（速度快、价格便宜）
- 国际用户：OpenAI GPT-4o-mini（性价比高）
- 预算有限：DeepSeek（价格最低）

### Q: 遇到连接错误怎么办？

**A:**
1. 运行 `python check_env.py` 检查配置
2. 确认 API Key 正确
3. 检查网络连接
4. 尝试使用阿里云服务（国内访问更稳定）

详细问题排查请查看 [配置指南](./CONFIG.md)

---

开始学习 → [01-plan-execute](./01-plan-execute/)
