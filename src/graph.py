from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, List, Annotated
import operator

# 1. Definisi State yang lebih kaya
class AgentState(TypedDict):
    messages: Annotated[List[str], operator.add]
    current_step: str
    data_found: bool

# 2. Definisi Nodes
def router_node(state: AgentState):
    print("--- ROUTING ---")
    last_msg = state['messages'][-1].lower() if state['messages'] else ""
    if 'izin' in last_msg:
        return "data_source"
    return "faq_source"

def faq_source_node(state: AgentState):
    print("--- FAQ NODE ---")
    return {"messages": ["Jawaban FAQ: Sistem CERDAS adalah asisten digital Kabupaten Semarang."], "current_step": "faq"}

def data_source_node(state: AgentState):
    print("--- DATA NODE ---")
    # Simulasi logika pencarian data (bisa dikembangkan ke SQL/API)
    return {"messages": ["Database: Informasi perizinan ditemukan (KTP & NIB)."], "data_found": True, "current_step": "data"}

# 3. Membangun Graph
workflow = StateGraph(AgentState)

workflow.add_node("router", router_node)
workflow.add_node("faq_source", faq_source_node)
workflow.add_node("data_source", data_source_node)

workflow.set_entry_point("router")

# Conditional edges
workflow.add_conditional_edges(
    "router", 
    router_node, 
    {"data_source": "data_source", "faq_source": "faq_source"}
)

workflow.add_edge("faq_source", END)
workflow.add_edge("data_source", END)

# Compile dengan Memory (Checkpointer)
checkpointer = MemorySaver()
app = workflow.compile(checkpointer=checkpointer)
