import uuid
import os
from dotenv import load_dotenv
from typing import List, Tuple

import google.generativeai as genai
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance, PointStruct

load_dotenv()

COLLECTION = "documents"

client = QdrantClient(host="qdrant", port=6333)

embedder = None

def get_embedder():
    global embedder
    if embedder is None:
        print("Loading embedding model...")
        embedder = SentenceTransformer("all-MiniLM-L6-v2")
    return embedder

def embed(texts: List[str]) -> List[List[float]]:
    return get_embedder().encode(texts).tolist()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    "gemini-2.5-flash",
    generation_config={
        "temperature": 0.2,
        "max_output_tokens": 256,
    }
)

def ask_llm(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text.strip()

def create_collection():
    client.recreate_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def ingest_text(text: str) -> int:
    chunks = chunk_text(text)
    vectors = embed(chunks)

    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=v,
            payload={"text": t}
        )
        for t, v in zip(chunks, vectors)
    ]

    client.upsert(COLLECTION, points)
    return len(points)

def search(query: str, top_k: int = 2) -> List[str]:
    query_vector = embed([query])[0]

    response = client.query_points(
        collection_name=COLLECTION,
        query=query_vector,
        limit=top_k
    )

    return [point.payload["text"] for point in response.points]

def trim_context(contexts: List[str], max_chars: int = 2500, max_chunks: int = 3) -> List[str]:
    trimmed = []
    total = 0

    for ctx in contexts[:max_chunks]:
        if total + len(ctx) > max_chars:
            break
        trimmed.append(ctx)
        total += len(ctx)

    return trimmed

def generate_answer(question: str, context: List[str]) -> str:
    safe_context = trim_context(context)
    context_text = "\n\n".join(safe_context)

    prompt = f"""
                You are an AI assistant.
                Answer ONLY using the context below.
                If the answer is not found, say: Information not found.

                CONTEXT:
                    {context_text}

                QUESTION:
                    {question}

                ANSWER:
            """
    try:
        return ask_llm(prompt)
    except Exception as e:
        return f"LLM Error: {str(e)}"

def ask(question: str) -> Tuple[str, List[str]]:
    contexts = search(question)

    if not contexts:
        contexts = ["No context available."]

    answer = generate_answer(question, contexts)

    return answer, contexts