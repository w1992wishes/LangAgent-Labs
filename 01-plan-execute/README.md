# 01-Plan-Execute Agent

使用 LangGraph 实现经典的 Plan-Execute 模式。

## 核心概念

**Plan-Execute 模式**：
1. **Plan**: 使用 LLM 分析任务并生成执行计划
2. **Execute**: 执行计划中的每个步骤
3. **Re-plan**: 根据执行结果决定是否需要重新规划

## 功能特性

- ✅ 使用 LLM 生成智能执行计划
- ✅ 逐步执行计划
- ✅ 支持流式和非流式输出
- ✅ RESTful API 接口
- ✅ 完整的状态管理

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置

确保在项目根目录有 `.env` 文件：

```
OPENAI_API_KEY=your-api-key-here
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
```

## 运行

启动 API 服务：

```bash
cd 01-plan-execute
python src/api.py
```

服务将在 http://localhost:8000 启动

## API 接口

### 1. 非流式接口

**POST** `/api/chat`

请求体：
```json
{
  "message": "帮我分析一下人工智能的发展趋势"
}
```

### 2. 流式接口

**POST** `/api/chat/stream`

请求体：
```json
{
  "message": "帮我分析一下人工智能的发展趋势"
}
```

返回 Server-Sent Events (SSE) 格式的流式数据

## 测试

使用 curl 测试：

```bash
# 非流式
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好"}'

# 流式
curl -X POST http://localhost:8000/api/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"message": "你好"}'
```

或访问 API 文档：http://localhost:8000/docs

## 核心代码结构

```
src/
├── state.py      # LangGraph 状态定义
├── prompts.py    # 提示词模板
├── graph.py      # LangGraph 工作流构建
└── api.py        # FastAPI 服务
```

## 学习要点

1. **State 管理**: 理解 LangGraph 中的状态流转
2. **节点设计**: Plan 和 Execute 节点的设计
3. **条件边**: 根据执行结果决定下一步
4. **流式输出**: 如何实现流式响应
