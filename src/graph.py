from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, List, Annotated
import operator
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage

# Inisialisasi
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-8b")
vectorstore = Chroma(persist_directory="./data/db", embedding_function=embeddings)

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]

def router_node(state: AgentState):
    return "retrieval"

def retrieval_node(state: AgentState):
    query = state['messages'][-1].content
    # Retrieval
    results = vectorstore.similarity_search(query, k=2)
    content = "\n".join([doc.page_content for doc in results]) if results else "Informasi tidak ditemukan."
    
    # Generation dengan Memory (mengirim seluruh history pesan)
    messages = [SystemMessage(content="Anda adalah asisten ramah Kabupaten Semarang. Gunakan riwayat percakapan berikut untuk memberikan jawaban kontekstual.")] + state['messages']
    
    response = llm.invoke(messages)
    
    return {"messages": [response]}

workflow = StateGraph(AgentState)
workflow.add_node("router", router_node)
workflow.add_node("retrieval", retrieval_node)
workflow.set_entry_point("router")
workflow.add_edge("router", "retrieval")
workflow.add_edge("retrieval", END)
app = workflow.compile(checkpointer=MemorySaver())
