from fastapi import FastAPI
from pydantic import BaseModel
from src.graph import app as graph_app

app = FastAPI()

class ChatRequest(BaseModel):
    query: str

@app.post("/chat")
async def chat(request: ChatRequest):
    # Invoke the graph
    result = graph_app.invoke({"query": request.query})
    return {"response": result.get("response", "Tidak ada jawaban.")}

@app.get("/")
def read_root():
    return {"message": "CERDAS API is ready for web widget"}
