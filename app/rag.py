import uuid
import os
from dotenv import load_dotenv

from huggingface_hub import InferenceClient
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance, PointStruct
from typing import List, Tuple

load_dotenv()

COLLECTION = "documents"

client = QdrantClient(host="qdrant", port=6333)
embedder = None
hf = InferenceClient(model="zai-org/GLM-4.7", token=os.getenv("HF_API_KEY"))

def create_collection():
    client.recreate_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )

def chunk_text(text: str, chunk_size: int = 250, overlap: int = 30) -> List[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def embed(texts: List[str]) -> List[List[float]]:
    global embedder
    if embedder is None:
        print("Loading embedding model...")
        embedder = SentenceTransformer('all-MiniLM-L6-v2')
    return embedder.encode(texts).tolist()

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

def generate_answer(question: str, context: List[str]) -> str:
    context_text = "\n".join(context[:2]) if context else "No context available."

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. Answer the question based on the provided context."
        },
        {
            "role": "user",
            "content": f"Context:\n{context_text}\n\nQuestion: {question}"
        }
    ]

    result = hf.chat_completion(
        messages=messages,
        max_tokens=120,
        temperature=0.2,
    )

    return result.choices[0].message.content.strip()

def ask(question: str) -> Tuple[str, List[str]]:
    """
    Search calling + generate_answer safely.
    Always Returns tuple (answer, contexts)
    """
    context = search(question)
    if not context:
        context = ["No context available."]
    answer = generate_answer(question, context)
    return answer, context