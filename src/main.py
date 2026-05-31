from fastapi import FastAPI
from pydantic import BaseModel
from src.graph import app as graph_app
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str

@app.post("/chat")
async def chat(request: ChatRequest):
    result = graph_app.invoke({"query": request.query})
    return {"response": result.get("response", "Tidak ada jawaban.")}

@app.get("/")
def read_root():
    return {"message": "CERDAS API is ready for web widget"}
