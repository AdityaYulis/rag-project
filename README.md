# 📚 RAG API – FastAPI + Qdrant + Gemini AI

This project is a **Retrieval Augmented Generation (RAG) API** that:
- Stores text into a **Qdrant vector database**
- Retrieves the most relevant context
- Generates answers using **Google Gemini AI (LLM)**

All services run using **Docker Compose**.

---

## 🚀 Features
- REST API with **FastAPI**
- Endpoints:
  - `POST /ingest` → store text into vector DB
  - `POST /ask` → ask questions to the RAG system
- **SentenceTransformer all-MiniLM-L6-v2** for embeddings
- **Qdrant** as vector database
- **Google Gemini API** as LLM generator
- Automatic text chunking
- Context trimming optimized for Gemini free tier
- Full Docker environment

---

## 🛠️ Technologies

| Component | Technology |
|----------|------------|
| API | FastAPI |
| Embedding | sentence-transformers (all-MiniLM-L6-v2) |
| Vector DB | Qdrant |
| LLM | Google Gemini API (gemini-2.5-flash) |
| Container | Docker, Docker Compose |

---

## 📂 Project Structure

```
rag-project/
│── app/
│   ├── main.py   # FastAPI entry point
│   └── rag.py    # RAG pipeline
│── .gitignore
│── Dockerfile
│── docker-compose.yml
│── requirements.txt
└── README.md
```

---

## 🔐 Gemini API Key Configuration

This project uses **Google Gemini API (NOT Hugging Face)**.

## Step 1 — Get API Key

Go to:

👉 https://aistudio.google.com/app/apikey

Create a new key.

---


## Step 2 — Create `.env`

Create a `.env` file in the project root:
```.env
GEMINI_API_KEY=your_api_key
```

## 💡 Free Tier Tips

Gemini free billing has request & token limits.  
This project is already optimized to avoid hitting limits:

- small output tokens (256)
- limited context size
- small top-k retrieval
- trimmed context
- low temperature

If you hit quota:
- wait a few minutes
- or upgrade billing

---

## ▶️ Running the Project

### 0. Prerequisites Check
Make sure Git and Docker are installed and active (You can Open **Docker Desktop** and make sure the staus shows **Running**)
```bash
git --version
docker --version
docker compose version
```
If all commands return a version number, you are ready to proceed.
```bash
git --version
  -> git version 2.53.0.windows.1
docker --version
  -> Docker version 29.2.0, build 0b9d198
docker compose version
  -> Docker Compose version v5.0.2
```


### 1. Clone the repository
```bash
git clone https://github.com/AdityaYulis/rag-project.git
cd rag-project
```

### 2. Start with Docker
```bash
docker compose up --build
```

### 3. Access the API
```
http://localhost:8000
```

Swagger UI:
```
http://localhost:8000/docs
```

## 📥 Ingest Data

```bash
curl -X POST http://localhost:8000/ingest      -H "Content-Type: application/json"      -d '{"text":"Your document text here"}'
```
---
**Or**
You can use Swagger UI to provides an interactive API Interface

### 1. Open Swagger UI
In your browser, go to:
``` bash
http://localhost:8000/docs
```
### 2. Click the endpoint: POST /ingset
This endpoint is used to send new data into the RAG system so it can be stored and searched later.

### 3. Click Try it out
This button allows you to manually test the API by sending a request from the browser.

### 4. In the request body, enter (example):
``` json
{
  "text": "Manchester United Football Club is a professional football club based in Old Trafford, Greater Manchester, England, and plays in the English Premier League."
}
```
This text will be split into chunks, converted into embeddings, and stored in the vector database.

**Note** : You can enter data/information about anything, as example i use informaiton about Manchester United

### 5. Click **Execute**
This sends the request to the server and starts the ingestion process.

### 6. If successfull, you will see :
``` json
{
  "ingested_chunks": 1
}
```

This means the text has been successfully stored in the vector database and is now ready to be queried.


<img width="1919" height="983" alt="Screenshot 2026-02-06 130946" src="https://github.com/user-attachments/assets/5e11be20-1818-4b9c-a507-fc605b4b5725" />

---

## ❓ Ask a Question

```bash
curl -X POST http://localhost:8000/ask      -H "Content-Type: application/json"      -d '{"question":"What is this document about?"}'
```

---
**Or**
You can use Swagger UI to provides an interactive API Interface

### 1. Click the endpoint: POST /ask
This endpoint is used to ask a question to the RAG system based on the data that has been ingested.

### 2. Click Try it out
This allows you to send a question directly from Swagger UI.

### 3. In the request body, enter (example) :
``` json
{
  "question": "What is Manchester United?"
}
```
This question will be converted into an embedding and compared with the stored data to find the most relevant context.

**Note** : You can ask about anything, as example i'm asking about Manchester United

### 4. Click **Execute**
The system will retrieve the best matching context from the vector database and send it to the LLM to generate an answer.

### 5. If successfull, you will see :
``` json
{
  "answer": "Manchester United Football Club is a professional football club based in Old Trafford, Greater Manchester, England, and plays in the English Premier League.",
  "contexts": [
    "Manchester United Football Club is a professional football club based in Old Trafford, Greater Manchester, England, and plays in the English Premier League."
  ]
}
```

When the Ask request is successful, the system converts the question into an embedding, searches the Qdrant vector database to find the most relevant document chunks, and sends those contexts to the Gemini LLM. The model then generates a final answer based on the retrieved information and returns it along with the source contexts.

<img width="1919" height="985" alt="image" src="https://github.com/user-attachments/assets/f550032d-52e1-4a2a-804a-1d7e4bf1fd11" />


---


## 🛑 Stop the Containers
```bash
docker compose down
```

---

## 👨‍💻 Author
**Aditya Yulis Kusdiyanto**  
