from fastapi import FastAPI
from src.graph import app
app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "CERDAS API Running"}
