"""
LangGraph 状态定义

定义 Plan-Execute Agent 的状态结构
"""
from typing import List, TypedDict, Annotated, Sequence, Optional, Callable
from langchain_core.messages import BaseMessage, HumanMessage
from operator import add


class PlanStep(TypedDict):
    """计划中的单个步骤"""
    step_id: int
    description: str
    status: str  # pending, in_progress, completed, failed


class AgentState(TypedDict):
    """Agent 主状态"""
    # 用户输入
    messages: Annotated[Sequence[BaseMessage], add]

    # 计划相关
    plan: List[PlanStep]  # 执行计划
    current_step_index: int  # 当前执行到哪一步

    # 执行结果
    steps_results: List[str]  # 每个步骤的执行结果
    final_response: str  # 最终响应

    # 控制标志
    is_planning: bool  # 是否正在规划
    is_executing: bool  # 是否正在执行
    is_finished: bool  # 是否完成

    # LLM 思考过程回调（可选）
    thinking_callback: Optional[Callable[[str, str], None]]  # (节点名, token) -> None


def create_initial_state(user_message: str, thinking_callback: Optional[Callable] = None) -> AgentState:
    """创建初始状态"""
    return {
        "messages": [HumanMessage(content=user_message)],
        "plan": [],
        "current_step_index": 0,
        "steps_results": [],
        "final_response": "",
        "is_planning": True,
        "is_executing": False,
        "is_finished": False,
        "thinking_callback": thinking_callback,
    }
