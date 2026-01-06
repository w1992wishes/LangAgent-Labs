# LLM 思考过程实时流式输出

## ✨ 新功能

现在可以看到 LLM 的实时思考过程！每个 token 生成时都会立即显示，让你看到 AI 的完整推理过程。

## 📊 效果演示

```
🚀 开始处理您的请求...

[PLAN] 我需要分析用户的需求，然后制定一个执行计划。
[PLAN] 根据用户的问题"你好"，我将直接生成一个友好的回答。
[PLAN] 步骤1: 分析用户意图
[PLAN] 步骤2: 生成友好回应

⏳ ✅ 已生成执行计划，共 2 个步骤

[EXECUTE] 你好！很高兴见到你～
[EXECUTE] 我是你的 AI 助手，准备帮助你。
[EXECUTE] 请告诉我你需要什么帮助。

⏳ ⚙️ 正在执行步骤 2/2: ...

[SYNTHESIZE] 综合以上结果...
[SYNTHESIZE] 你好！我是 AI 助手...

🎯 最终结果
...
```

## 🎯 核心实现

### 1. **状态管理** (state.py)
```python
thinking_callback: Optional[Callable[[str, str], None]]  # (节点名, token) -> None
```

### 2. **节点实现** (graph.py)
使用 `llm.astream()` 替代 `llm.ainvoke()`：
```python
async for chunk in llm.astream(prompt):
    token = chunk.content
    full_response += token

    # 调用回调，实时发送思考过程
    if thinking_callback:
        thinking_callback("plan", token)
```

### 3. **API 层** (api.py)
使用 `asyncio.Queue` 并发处理：
- **任务1**: 执行 LangGraph 图
- **任务2**: 从队列读取思考事件并发送

### 4. **SSE 事件流**
```javascript
// 新增 thinking 事件
{event: "thinking", data: "[PLAN] 我需要分析..."}

// 原有事件保持不变
{event: "start", data: "..."}
{event: "progress", data: "..."}
{event: "final", data: {...}}
```

## 🚀 使用方式

### 测试流式输出
```bash
python test_api.py
```

### API 调用
```bash
curl -X POST http://localhost:8000/api/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"message": "你好"}'
```

## 📝 技术亮点

1. **真正的流式输出**: 使用 `llm.astream()` 获取每个 token
2. **并发处理**: `asyncio.Queue` + `asyncio.create_task`
3. **非阻塞**: 图执行和思考事件并行处理
4. **完整日志**: 保留所有服务端日志

## 🔜 与之前版本对比

| 特性 | 之前 | 现在 |
|------|------|------|
| 输出方式 | 等待节点完成 | 实时显示每个 token |
| 用户体验 | 黑盒等待 | 透明的思考过程 |
| 信息量 | 只有最终结果 | 完整推理过程 |

## 💡 应用场景

1. **教育场景**: 让学生看到 AI 的思考过程
2. **调试**: 观察 LLM 如何理解和处理问题
3. **透明度**: 用户了解 AI 的决策过程
4. **交互**: 更好的实时反馈

---

**分支**: `feature/llm-thinking-stream`
**提交**: `ee007fa`
