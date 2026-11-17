# CareerCraft Backend

AI-powered career guidance platform built with **FastAPI**, **ChromaDB**, **sentence-transformers**, and **Ollama**.

---

## Architecture

```
careercraft/
├── main.py                  # FastAPI app + lifespan startup
├── requirements.txt
├── models/
│   ├── schemas.py           # Pydantic request/response models
│   └── user_store.py        # In-memory user store (swap → PostgreSQL)
├── services/
│   ├── skill_gap.py         # Skill gap analysis logic
│   ├── vector_store.py      # ChromaDB embedding + retrieval
│   └── rag_advisor.py       # RAG pipeline → Ollama LLM
├── routers/
│   ├── users.py             # POST/GET /users
│   ├── skill_gap.py         # POST /skill-gap
│   ├── search.py            # POST /search
│   └── advisory.py          # POST /advisory
└── data/
    └── chromadb/            # Persistent vector DB (auto-created)
```

---

## Setup

### 1. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 2. Install and start Ollama
```bash
# macOS/Linux
curl -fsSL https://ollama.com/install.sh | sh
ollama serve                  # keep this running in a terminal
ollama pull llama3            # or: mistral, phi3, gemma
```

### 3. Start the API server
```bash
uvicorn main:app --reload --port 8000
```

### 4. Open interactive docs
```
http://localhost:8000/docs
```

---

## API Endpoints

### User Profiles
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/` | Register a new user |
| GET | `/users/{id}` | Get user by ID |
| GET | `/users/` | List all users |

### Skill Gap Analysis
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/skill-gap/` | Analyze skill gap for a target role |
| GET | `/skill-gap/roles` | List supported career roles |

### Semantic Retrieval
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/search/` | Semantic search over career knowledge |
| POST | `/search/documents` | Ingest a new document into ChromaDB |

### RAG Advisory
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/advisory/` | Get personalized AI career advice |

---

## Example Usage

### Register a user
```bash
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Priya Sharma",
    "email": "priya@example.com",
    "education": "B.Tech Computer Science",
    "technical_skills": ["python", "sql", "pandas", "scikit-learn"],
    "certifications": [{"name": "Google Data Analytics", "issuer": "Google", "year": 2023}],
    "work_experience": [],
    "career_interests": ["data scientist", "ml engineer"],
    "experience_level": "fresher"
  }'
```

### Run skill gap analysis
```bash
curl -X POST http://localhost:8000/skill-gap/ \
  -H "Content-Type: application/json" \
  -d '{"user_id": "<id-from-above>", "target_role": "data scientist"}'
```

### Ask for career advice
```bash
curl -X POST http://localhost:8000/advisory/ \
  -H "Content-Type: application/json" \
  -d '{"user_id": "<id-from-above>", "question": "What should I learn to become a data scientist in 6 months?"}'
```

---

## Switching LLM Models

Edit `services/rag_advisor.py`:
```python
OLLAMA_MODEL = "llama3"    # or "mistral", "phi3", "gemma2", "codellama"
```

---

## Production Upgrades (Next Steps)

- [ ] Replace in-memory store → **PostgreSQL + SQLAlchemy**
- [ ] Add **JWT authentication** (fastapi-users)
- [ ] Swap seed data → **real job postings** (LinkedIn / Indeed API)
- [ ] Add **embedding caching** for performance
- [ ] Deploy with **Docker Compose** (API + ChromaDB + Ollama)
- [ ] Add **async background jobs** for heavy embedding tasks (Celery / ARQ)
