from typing import TypedDict, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

from src.config import Config
from src.orchestrator.tools import run_audit_query, run_custom_cypher



class AgentState(TypedDict):
    messages: List[str]
    final_report: str


# 2. Initialize Models & Tools
llm = ChatGoogleGenerativeAI(model=Config.MODEL_NAME, google_api_key=Config.GEMINI_API_KEY)
tools = [run_audit_query, run_custom_cypher]
llm_with_tools = llm.bind_tools(tools)


# 3. Define Nodes
def reasoner(state: AgentState):
    """The Brain: Decides whether to call a tool or finish."""
    messages = state['messages']


    system_prompt = SystemMessage(content="""
    You are AuditGraph AI. Your goal is to find fraud in the database.
    1. Start by running standard audit queries using the 'run_audit_query' tool.
    2. If you find a specific person/company, use 'run_custom_cypher' to dig deeper.
    3. Once you have evidence (or lack of it), output a Final Report.
    """)

    # Prepare input for LLM
    response = llm_with_tools.invoke([system_prompt] + messages)
    return {"messages": [response]}


def executor(state: AgentState):
    """The Hands: Executes the tool calls decided by the reasoner."""
    last_message = state['messages'][-1]

    if not last_message.tool_calls:
        # If no tool called, we are done
        return {"final_report": last_message.content}

    results = []
    for tool_call in last_message.tool_calls:
        tool_name = tool_call['name']
        tool_args = tool_call['args']

        # Route to correct function
        if tool_name == "run_audit_query":
            output = run_audit_query.invoke(tool_args)
        elif tool_name == "run_custom_cypher":
            output = run_custom_cypher.invoke(tool_args)
        else:
            output = "Unknown Tool"

        # Create a message representing the tool output
        results.append(HumanMessage(content=f"Tool '{tool_name}' Output: {output}"))

    return {"messages": results}



workflow = StateGraph(AgentState)

workflow.add_node("reasoner", reasoner)
workflow.add_node("executor", executor)

workflow.set_entry_point("reasoner")


def should_continue(state: AgentState):
    last_message = state['messages'][-1]
    if last_message.tool_calls:
        return "executor"
    return END


workflow.add_conditional_edges("reasoner", should_continue)
workflow.add_edge("executor", "reasoner")

audit_bot = workflow.compile()