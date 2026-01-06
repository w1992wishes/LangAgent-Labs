"""
FastAPI 服务

提供流式和非流式 API 接口
"""
import os
import json
import logging
import asyncio
from typing import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
from dotenv import load_dotenv

from .graph import graph
from .state import create_initial_state

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 请求模型
class ChatRequest(BaseModel):
    message: str


# 响应模型
class ChatResponse(BaseModel):
    response: str
    plan: list[dict]
    steps_results: list[str]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    logger.info("=" * 60)
    logger.info("🚀 Plan-Execute Agent API 启动中...")
    logger.info(f"📝 模型: {os.getenv('OPENAI_MODEL', 'qwen-plus')}")
    logger.info(f"🌐 API 地址: http://localhost:8000")
    logger.info(f"📖 API 文档: http://localhost:8000/docs")
    logger.info("=" * 60)
    yield
    logger.info("👋 Plan-Execute Agent API 已关闭")


# 创建 FastAPI 应用
app = FastAPI(
    title="Plan-Execute Agent API",
    description="基于 LangGraph 的 Plan-Execute 模式实现",
    version="1.0.0",
    lifespan=lifespan
)

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Plan-Execute Agent API",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/api/chat",
            "chat_stream": "/api/chat/stream",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health():
    """健康检查"""
    return {"status": "healthy"}


async def stream_graph_events(user_message: str) -> AsyncGenerator[dict, None]:
    """流式输出图事件（包含 LLM 思考过程）"""
    try:
        logger.info(f"📥 [流式] 收到请求: {user_message}")

        # 创建队列用于传递思考事件
        thinking_queue = asyncio.Queue()

        # 定义思考回调函数
        def thinking_callback(node_name: str, token: str):
            """LLM 思考过程回调"""
            thinking_queue.put_nowait({
                "node": node_name,
                "token": token
            })

        # 创建初始状态，传入思考回调
        initial_state = create_initial_state(user_message, thinking_callback)

        # 立即发送开始事件
        yield {
            "event": "start",
            "data": "开始处理您的请求..."
        }

        # 创建异步任务：执行图并收集结果
        async def run_graph():
            """执行图并收集最终状态"""
            result_state = {}
            async for event in graph.astream(initial_state):
                for node_name, node_output in event.items():
                    if isinstance(node_output, dict):
                        result_state.update(node_output)
            return result_state

        # 启动图执行任务
        graph_task = asyncio.create_task(run_graph())

        # 同时处理思考事件
        while not graph_task.done():
            # 尝试获取思考事件（带超时）
            try:
                thinking_event = await asyncio.wait_for(thinking_queue.get(), timeout=0.05)
                node_name = thinking_event["node"]
                token = thinking_event["token"]

                yield {
                    "event": "thinking",
                    "data": f"[{node_name.upper()}] {token}"
                }
            except asyncio.TimeoutError:
                # 没有思考事件，继续循环
                continue

        # 图执行完成，处理剩余的思考事件
        while not thinking_queue.empty():
            thinking_event = thinking_queue.get_nowait()
            node_name = thinking_event["node"]
            token = thinking_event["token"]
            yield {
                "event": "thinking",
                "data": f"[{node_name.upper()}] {token}"
            }

        # 获取最终结果
        final_state = await graph_task

        logger.info(f"✅ [流式] 执行完成")
        logger.info(f"📤 [流式] 最终回答长度: {len(final_state.get('final_response', ''))} 字符")

        # 发送最终结果
        yield {
            "event": "final",
            "data": {
                "response": final_state.get("final_response", ""),
                "plan": final_state.get("plan", []),
                "steps_results": final_state.get("steps_results", [])
            }
        }

    except Exception as e:
        logger.error(f"❌ [流式] 错误: {str(e)}", exc_info=True)
        yield {
            "event": "error",
            "data": {"error": str(e)}
        }


def sanitize_output(output: dict) -> dict:
    """清理输出数据，使其可序列化为 JSON"""
    sanitized = {}
    for key, value in output.items():
        if isinstance(value, (str, int, float, bool, list, dict)):
            sanitized[key] = value
        elif hasattr(value, "content"):  # Message 对象
            sanitized[key] = value.content
        else:
            sanitized[key] = str(value)
    return sanitized


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    非流式聊天接口

    完整执行 Plan-Execute 流程后返回结果
    """
    try:
        logger.info("=" * 60)
        logger.info(f"📥 [非流式] 收到请求")
        logger.info(f"💬 消息内容: {request.message[:100]}...")
        logger.info("-" * 60)

        # 创建初始状态
        initial_state = create_initial_state(request.message)

        # 执行图
        result = await graph.ainvoke(initial_state)

        logger.info("-" * 60)
        logger.info(f"✅ [非流式] 执行完成")
        logger.info(f"📋 计划步骤数: {len(result.get('plan', []))}")
        logger.info(f"📝 执行步骤数: {len(result.get('steps_results', []))}")
        logger.info(f"📤 最终回答长度: {len(result.get('final_response', ''))} 字符")
        logger.info("=" * 60)

        return ChatResponse(
            response=result.get("final_response", ""),
            plan=result.get("plan", []),
            steps_results=result.get("steps_results", [])
        )

    except Exception as e:
        logger.error(f"❌ [非流式] 错误: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    流式聊天接口

    使用 Server-Sent Events (SSE) 实时返回执行过程
    """
    async def event_generator():
        try:
            logger.info(f"📥 [流式] 开始处理请求: {request.message}")

            async for event_dict in stream_graph_events(request.message):
                # 确保 event_dict 是可序列化的
                if isinstance(event_dict, dict):
                    event_type = event_dict.get("event", "")
                    event_data = event_dict.get("data", "")

                    # 直接转发所有事件
                    if event_type in ["start", "progress"]:
                        # 进度事件：data 是字符串
                        logger.info(f"📤 [流式] 发送 {event_type} 事件: {event_data}")
                        yield {
                            "event": event_type,
                            "data": event_data
                        }
                    elif event_type == "final":
                        # 最终事件：data 是完整的结构化数据（和非流式一样）
                        response_text = event_data.get("response", "")
                        plan = event_data.get("plan", [])
                        logger.info(f"✅ [流式] 发送 final 事件")
                        logger.info(f"   - 计划步骤数: {len(plan)}")
                        logger.info(f"   - 回答长度: {len(response_text)} 字符")
                        logger.info(f"   - 计划内容:")
                        for step in plan:
                            logger.info(f"      {step.get('step_id', '-')}. {step.get('description', '')}")
                        yield {
                            "event": "final",
                            "data": event_data  # 完整的结构化数据
                        }
                    elif event_type == "error":
                        error_msg = event_data.get("error", "Unknown error") if isinstance(event_data, dict) else event_data
                        logger.error(f"❌ [流式] 发送 error 事件: {error_msg}")
                        yield {
                            "event": "error",
                            "data": error_msg
                        }

            logger.info(f"✅ [流式] 请求处理完成")

        except Exception as e:
            logger.error(f"❌ [流式生成器] 错误: {str(e)}", exc_info=True)
            yield {
                "event": "error",
                "data": str(e)
            }

    return EventSourceResponse(
        event_generator(),
        media_type="text/event-stream",
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
