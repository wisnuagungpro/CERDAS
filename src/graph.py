from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Annotated
import operator

class AgentState(TypedDict):
    messages: Annotated[List[str], operator.add]
    data: dict

def node_router(state: AgentState):
    print("Routing query...")
    return "answer"

def node_answer(state: AgentState):
    print("Generating answer...")
    return {"messages": ["Dummy response for CERDAS"]}

workflow = StateGraph(AgentState)
workflow.add_node("router", node_router)
workflow.add_node("answer", node_answer)
workflow.add_edge("router", "answer")
workflow.add_edge("answer", END)
workflow.set_entry_point("router")
app = workflow.compile()
