"""
LangGraph 工作流定义

实现 Plan-Execute 模式的核心逻辑
"""
import os
import re
import logging
from typing import Literal
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph, END

from .state import AgentState, PlanStep
from .prompts import PLANNER_PROMPT, EXECUTOR_PROMPT, SYNTHESIZER_PROMPT

# 配置日志
logger = logging.getLogger(__name__)

# 初始化 LLM
llm = ChatOpenAI(
    model=os.getenv("DASHSCOPE_MODEL", "qwen-plus"),
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("DASHSCOPE_API_BASE", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
    temperature=0.1,
)

# llm = ChatOpenAI(
#     temperature=0.1,
#     model="glm-4.7",
#     api_key=os.getenv("ZHIPU_API_KEY"),
#     base_url=os.getenv("ZHIPU_API_BASE", "https://open.bigmodel.cn/api/paas/v4/"),
# )


def parse_plan_steps(plan_text: str) -> list[PlanStep]:
    """解析 LLM 生成的计划文本，提取出步骤列表"""
    steps = []
    lines = plan_text.strip().split('\n')

    for line in lines:
        line = line.strip()
        # 匹配 "步骤 1: 描述" 或 "1. 描述" 格式
        match = re.match(r'(?:步骤\s*)?(\d+)[\.:：]\s*(.+)', line)
        if match:
            step_id = int(match.group(1))
            description = match.group(2).strip()
            steps.append(PlanStep(
                step_id=step_id,
                description=description,
                status="pending"
            ))

    return steps


async def plan_node(state: AgentState) -> AgentState:
    """规划节点：使用 LLM 生成执行计划"""
    logger.info("🎯 [PLAN 节点] 开始生成执行计划...")
    user_input = state["messages"][-1].content

    # 使用 LLM 生成计划
    prompt = PLANNER_PROMPT.format(input=user_input)
    logger.info(f"📝 [PLAN 节点] 调用 LLM 生成计划...")
    response = await llm.ainvoke(prompt)

    logger.info(f"📄 [PLAN 节点] LLM 原始响应:\n{response.content[:500]}...")

    # 解析计划
    plan_steps = parse_plan_steps(response.content)

    # 如果没有解析到步骤，创建一个默认步骤
    if not plan_steps:
        logger.warning("⚠️  [PLAN 节点] 未能解析步骤，使用默认步骤")
        plan_steps = [PlanStep(
            step_id=1,
            description="直接回答用户的问题",
            status="pending"
        )]

    logger.info(f"✅ [PLAN 节点] 成功生成 {len(plan_steps)} 个步骤:")
    for i, step in enumerate(plan_steps, 1):
        logger.info(f"   {i}. {step['description']}")

    return {
        "plan": plan_steps,
        "current_step_index": 0,
        "is_planning": False,
        "is_executing": True,
    }


async def execute_node(state: AgentState) -> AgentState:
    """执行节点：执行当前步骤"""
    plan = state["plan"]
    current_index = state["current_step_index"]

    if current_index >= len(plan):
        logger.info(f"⏭️  [EXECUTE 节点] 所有步骤已完成，准备进入综合阶段")
        return {
            "is_executing": False,
            "is_finished": True,
        }

    current_step = plan[current_index]
    logger.info(f"⚙️  [EXECUTE 节点] 执行步骤 {current_index + 1}/{len(plan)}: {current_step['description']}")

    user_input = state["messages"][-1].content
    completed_steps = state["steps_results"]

    # 构建执行提示
    completed_info = "\n".join([
        f"- {plan[i]['description']}: {result}"
        for i, result in enumerate(completed_steps)
    ]) if completed_steps else "无"

    prompt = EXECUTOR_PROMPT.format(
        user_input=user_input,
        completed_steps=completed_info,
        current_step=current_step["description"]
    )

    # 执行步骤
    logger.info(f"📝 [EXECUTE 节点] 调用 LLM 执行步骤...")
    response = await llm.ainvoke(prompt)
    result = response.content

    logger.info(f"✅ [EXECUTE 节点] 步骤执行完成")
    logger.info(f"📄 [EXECUTE 节点] 执行结果预览: {result[:200]}...")

    # 更新步骤状态和结果
    updated_plan = [
        {**step, "status": "completed" if i == current_index else step["status"]}
        for i, step in enumerate(plan)
    ]

    updated_results = state["steps_results"] + [result]

    return {
        "plan": updated_plan,
        "steps_results": updated_results,
        "current_step_index": current_index + 1,
    }


async def synthesize_node(state: AgentState) -> AgentState:
    """综合节点：将所有步骤的结果整合成最终回答"""
    logger.info("🔄 [SYNTHESIZE 节点] 开始综合所有步骤的结果...")
    user_input = state["messages"][-1].content
    plan = state["plan"]
    steps_results = state["steps_results"]

    logger.info(f"📊 [SYNTHESIZE 节点] 需要综合 {len(steps_results)} 个步骤的结果")

    # 构建计划描述
    plan_info = "\n".join([
        f"{i+1}. {step['description']}"
        for i, step in enumerate(plan)
    ])

    # 构建结果描述
    results_info = "\n".join([
        f"步骤 {i+1} - {plan[i]['description']}\n结果: {result}\n"
        for i, result in enumerate(steps_results)
    ])

    # 使用 LLM 综合结果
    logger.info(f"📝 [SYNTHESIZE 节点] 调用 LLM 综合结果...")
    prompt = SYNTHESIZER_PROMPT.format(
        user_input=user_input,
        plan=plan_info,
        steps_results=results_info
    )

    response = await llm.ainvoke(prompt)

    logger.info(f"✅ [SYNTHESIZE 节点] 综合完成")
    logger.info(f"📄 [SYNTHESIZE 节点] 最终回答预览: {response.content[:300]}...")
    logger.info(f"📏 [SYNTHESIZE 节点] 最终回答长度: {len(response.content)} 字符")

    return {
        "final_response": response.content,
        "is_finished": True,
    }


def should_continue_executing(state: AgentState) -> Literal["execute", "synthesize"]:
    """判断是否继续执行还是进入综合阶段"""
    current_index = state["current_step_index"]
    total_steps = len(state["plan"])

    if current_index >= total_steps:
        logger.info(f"🔀 [条件边] 所有步骤已完成，进入综合阶段")
        return "synthesize"

    logger.info(f"🔀 [条件边] 继续执行步骤 {current_index + 1}/{total_steps}")
    return "execute"


def create_graph() -> StateGraph:
    """创建 Plan-Execute 工作流图"""
    workflow = StateGraph(AgentState)

    # 添加节点
    workflow.add_node("plan", plan_node)
    workflow.add_node("execute", execute_node)
    workflow.add_node("synthesize", synthesize_node)

    # 设置入口点
    workflow.set_entry_point("plan")

    # 添加边
    workflow.add_edge("plan", "execute")
    workflow.add_conditional_edges(
        "execute",
        should_continue_executing,
        {
            "execute": "execute",
            "synthesize": "synthesize",
        }
    )
    workflow.add_edge("synthesize", END)

    return workflow.compile()


# 创建全局图实例
graph = create_graph()
