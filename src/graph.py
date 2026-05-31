from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
import json

class AgentState(TypedDict):
    query: str
    response: str

def load_data():
    with open("data/database.json", "r") as f:
        return json.load(f)

def router_node(state: AgentState):
    query = state['query'].lower()
    if 'izin' in query or 'syarat' in query:
        return "data_source"
    return "faq_source"

def faq_source_node(state: AgentState):
    return {"response": "FAQ: CERDAS adalah asisten digital Kabupaten Semarang."}

def data_source_node(state: AgentState):
    data = load_data()
    for item in data:
        if item['topic'] == 'perizinan':
            return {"response": f"Database: {item['info']}"}
    return {"response": "Data tidak ditemukan."}

workflow = StateGraph(AgentState)
workflow.add_node("router", router_node)
workflow.add_node("faq_source", faq_source_node)
workflow.add_node("data_source", data_source_node)
workflow.set_entry_point("router")
workflow.add_conditional_edges("router", router_node, {"data_source": "data_source", "faq_source": "faq_source"})
workflow.add_edge("faq_source", END)
workflow.add_edge("data_source", END)
app = workflow.compile()
