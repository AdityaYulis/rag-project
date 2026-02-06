# 📚 RAG API -- FastAPI + Qdrant + Gemini AI

This project is a **Retrieval Augmented Generation (RAG) API** that:

-   Stores documents into a **Qdrant vector database**
-   Finds the most relevant chunks using embeddings
-   Generates answers using **Google Gemini AI (LLM)**

All services run using **Docker Compose** so the project is easy to
start and reproducible on any machine.

------------------------------------------------------------------------

## 🚀 Features

-   REST API with **FastAPI**
-   Endpoints:
    -   `POST /ingest` → store text into vector DB
    -   `POST /ask` → ask questions to the RAG system
-   **SentenceTransformer all-MiniLM-L6-v2** for embeddings
-   **Qdrant** as vector database
-   **Google Gemini API** as answer generator (LLM)
-   Automatic text chunking
-   Context trimming (optimized for free tier usage)
-   Full Docker environment (one command run)

------------------------------------------------------------------------

## 🛠️ Technologies

  Component   Technology
  ----------- ------------------------------------------
  API         FastAPI
  Embedding   sentence-transformers (all-MiniLM-L6-v2)
  Vector DB   Qdrant
  LLM         Google Gemini API (gemini-flash series)
  Container   Docker, Docker Compose

------------------------------------------------------------------------

## 📂 Project Structure

    rag-project/
    │── app/
    │   ├── main.py   # FastAPI entry point
    │   └── rag.py    # RAG pipeline (Gemini + Qdrant)
    │── .gitignore
    │── Dockerfile
    │── docker-compose.yml
    │── requirements.txt
    └── README.md

------------------------------------------------------------------------

# 🔐 Gemini API Key Configuration

This project uses **Google Gemini AI**, NOT Hugging Face anymore.

## Step 1 --- Create API Key

Open:

https://aistudio.google.com/app/apikey

Generate a new API key.

------------------------------------------------------------------------

## Step 2 --- Create `.env` file

Create `.env` in the project root:

    GEMINI_API_KEY=your_api_key_here

Docker automatically loads this key because `docker-compose.yml` already
includes:

    env_file:
      - .env

------------------------------------------------------------------------

## 💡 Free Tier Optimization

Gemini free billing has request & token limits.

This project is already optimized to avoid quota errors:

-   small output tokens (256)
-   limited context size
-   small top-k retrieval
-   trimmed context
-   low temperature

If you hit quota: - wait a few minutes - or upgrade billing

------------------------------------------------------------------------

# ▶️ Running the Project

## 0. Prerequisites Check

Make sure Git and Docker are installed and running:

    git --version
    docker --version
    docker compose version

Example:

    git version 2.x.x
    Docker version 29.x.x
    Docker Compose version v5.x.x

If all commands return a version number, you are ready to proceed.

------------------------------------------------------------------------

## 1. Clone the repository

    git clone https://github.com/AdityaYulis/rag-project.git
    cd rag-project

------------------------------------------------------------------------

## 2. Start with Docker

IMPORTANT: always use `--build` when dependencies change

    docker compose up --build

------------------------------------------------------------------------

## 3. Access the API

Main URL:

    http://localhost:8000

Swagger UI:

    http://localhost:8000/docs

Swagger provides an interactive interface to test all endpoints easily.

------------------------------------------------------------------------

# 📥 Ingest Data

Store text into the vector database.

### Using curl

    curl -X POST http://localhost:8000/ingest \
    -H "Content-Type: application/json" \
    -d '{"text":"Your document text here"}'

------------------------------------------------------------------------

### Using Swagger UI

### 1. Open Swagger

    http://localhost:8000/docs

### 2. Click endpoint: POST /ingest

This endpoint sends new data into the RAG system so it can be stored and
searched later.

### 3. Click Try it out

### 4. Example body

    {
      "text": "Manchester United Football Club is a professional football club based in Old Trafford, Greater Manchester, England, and plays in the English Premier League."
    }

### 5. Click Execute

### 6. Success response

    {
      "ingested_chunks": 1
    }

This means the text has been split into chunks, embedded, and stored in
Qdrant.

------------------------------------------------------------------------

# ❓ Ask a Question

Query the stored knowledge.

### Using curl

    curl -X POST http://localhost:8000/ask \
    -H "Content-Type: application/json" \
    -d '{"question":"What is Manchester United?"}'

------------------------------------------------------------------------

### Using Swagger UI

### 1. Click POST /ask

This endpoint sends a question to the RAG system.

### 2. Click Try it out

### 3. Example body

    {
      "question": "What is Manchester United?"
    }

### 4. Click Execute

### 5. Example response

    {
      "answer": "Manchester United is a professional football club based in Old Trafford, Greater Manchester, England.",
      "contexts": [
        "Manchester United Football Club is a professional football club based in Old Trafford, Greater Manchester, England."
      ]
    }

The system: - converts question to embedding - searches Qdrant -
retrieves relevant chunks - sends context to Gemini - Gemini generates
final answer

------------------------------------------------------------------------

# ⚙️ How It Works (Architecture)

    User Question
       ↓
    SentenceTransformer Embedding
       ↓
    Qdrant Vector Search
       ↓
    Context Retrieval
       ↓
    Gemini AI Generation
       ↓
    Answer

------------------------------------------------------------------------

# 🛑 Stop the Containers

    docker compose down

------------------------------------------------------------------------

# 👨‍💻 Author

Aditya Yulis Kusdiyanto
