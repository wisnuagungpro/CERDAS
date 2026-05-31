from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, List, Annotated
import operator
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Inisialisasi Vector Store
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vectorstore = Chroma(persist_directory="./data/db", embedding_function=embeddings)

class AgentState(TypedDict):
    messages: Annotated[List[str], operator.add]
    current_step: str

def router_node(state: AgentState):
    return "retrieval"

def retrieval_node(state: AgentState):
    query = state['messages'][-1]
    # Mencari 2 dokumen paling relevan
    results = vectorstore.similarity_search(query, k=2)
    content = "\n".join([doc.page_content for doc in results]) if results else "Informasi tidak ditemukan."
    return {"messages": [f"Hasil pencarian dokumen: {content}"], "current_step": "retrieval"}

workflow = StateGraph(AgentState)
workflow.add_node("router", router_node)
workflow.add_node("retrieval", retrieval_node)
workflow.set_entry_point("router")
workflow.add_edge("router", "retrieval")
workflow.add_edge("retrieval", END)
app = workflow.compile(checkpointer=MemorySaver())
