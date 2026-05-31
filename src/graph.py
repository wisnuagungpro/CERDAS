from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    query: str
    response: str
    data_source: str

def router_node(state: AgentState):
    query = state['query'].lower()
    if 'data' in query:
        return "data_source"
    return "faq_source"

def faq_source_node(state: AgentState):
    return {"response": "Jawaban dari FAQ: Sistem CERDAS adalah asisten Kabupaten Semarang."}

def data_source_node(state: AgentState):
    return {"response": "Jawaban dari Database: Data yang Anda minta ditemukan."}

workflow = StateGraph(AgentState)
workflow.add_node("router", router_node)
workflow.add_node("faq_source", faq_source_node)
workflow.add_node("data_source", data_source_node)

workflow.set_entry_point("router")
workflow.add_conditional_edges("router", router_node, {"data_source": "data_source", "faq_source": "faq_source"})
workflow.add_edge("faq_source", END)
workflow.add_edge("data_source", END)

app = workflow.compile()
