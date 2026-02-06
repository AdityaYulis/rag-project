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

def safe_ask(question: str) -> Tuple[str, List[str]]:
    """
    Safely calling rag.ask.
    Always returns a tuple (answer, contexts).
    """
    result = rag.ask(question)

    if not result:
        return "No answer found", []

    try:
        answer, contexts = result
        if not isinstance(contexts, list):
            contexts = [contexts]
        return answer, contexts
    except ValueError:
        return result, []

@app.post("/ingest")
def ingest(request: IngestRequest):
    count = rag.ingest_text(request.text)
    return {"ingested_chunks": count}

@app.post("/ask")
def ask(req: AskRequest):
    answer, contexts = safe_ask(req.question)
    return {"answer": answer, "contexts": contexts}
