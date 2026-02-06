# 📚 RAG API – FastAPI + Qdrant + Hugging Face

This project is a **Retrieval Augmented Generation (RAG) API** that:
- Stores text into a **Qdrant vector database**
- Retrieves the most relevant context
- Generates answers using **Hugging Face LLM (GLM-4.7)**

All services run using **Docker Compose**.

---

## 🚀 Features
- REST API with **FastAPI**
- Endpoints:
  - `POST /ingest` → store text into vector DB
  - `POST /ask` → ask questions to the RAG system
- **SentenceTransformer all-MiniLM-L6-v2** for embeddings
- **Qdrant** as vector database
- **Hugging Face Inference API** as LLM generator
- Automatic text chunking
- Full Docker environment

---

## 🛠️ Technologies

| Component | Technology |
|----------|------------|
| API | FastAPI |
| Embedding | sentence-transformers (all-MiniLM-L6-v2) |
| Vector DB | Qdrant |
| LLM | Hugging Face Inference API (zai-org/GLM-4.7) |
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

## 🔐 Hugging Face Token Configuration

Create a `.env` file in the project root and add
```env
HF_API_KEY=hf_xxxxxxxxxxxxx
```
---

You can generate your own API with Hugging Face https://huggingface.co/settings/tokens

<img width="244" height="213" alt="image" src="https://github.com/user-attachments/assets/aafcd869-037a-46bc-94e3-19bf92aa3388" />

Make sure your permission same as the picture

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

## ❓ Ask a Question

```bash
curl -X POST http://localhost:8000/ask      -H "Content-Type: application/json"      -d '{"question":"What is this document about?"}'
```

---

## 🛑 Stop the Containers
```bash
docker compose down
```

---

## 👨‍💻 Author
**Aditya Yulis Kusdiyanto**  
Machine Learning & Data Science Enthusiast
