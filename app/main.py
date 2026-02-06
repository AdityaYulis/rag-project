from fastapi import FastAPI
from pydantic import BaseModel
import rag
from typing import Tuple, List

app = FastAPI()

rag.create_collection()

class IngestRequest(BaseModel):
    text: str

class AskRequest(BaseModel):
    question: str

@app.post("/ingest")
def ingest(request: IngestRequest):
    count = rag.ingest_text(request.text)
    return {"ingested_chunks": count}

@app.post("/ask")
def ask(req: AskRequest):
    try:
        answer, contexts = rag.ask(req.question)
        if not contexts:
            contexts = ["No context available."]
        if not answer:
            answer = "Information not found."
    except Exception as e:
        answer = f"Error: {e}"
        contexts = []
    return {"answer": answer, "contexts": contexts}
