from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from src.graph import app as graph_app
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str

@app.post("/chat")
async def chat(request: ChatRequest):
    result = graph_app.invoke({"messages": [request.query]})
    return {"response": result['messages'][-1].content}

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    # Menggunakan OpenAI Whisper API (jauh lebih ringan dari lokal)
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=file.file
    )
    return {"text": transcript.text}

@app.get("/")
def read_root():
    return {"message": "CERDAS API with VTT (API Based) ready"}
