"""
CareerCraft Backend
===================
Run with:  uvicorn main:app --reload --port 8000
Docs at:   http://localhost:8000/docs
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from routers import users, skill_gap, search, advisory
from services.vector_store import seed_knowledge_base
from routers import resume          # add this import


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: seed ChromaDB if empty
    count = seed_knowledge_base()
    if count:
        print(f"✅  Seeded {count} documents into ChromaDB knowledge base.")
    else:
        print("✅  ChromaDB already populated — skipping seed.")
    yield
    # Shutdown (add cleanup here if needed)


app = FastAPI(
    title="CareerCraft API",
    description=(
        "AI-powered career guidance platform with skill gap analysis, "
        "semantic retrieval, and RAG-based advisory using Ollama + ChromaDB."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register routers ───────────────────────────────────────────────────────────
app.include_router(users.router)
app.include_router(skill_gap.router)
app.include_router(search.router)
app.include_router(advisory.router)
app.include_router(resume.router)   
@app.get("/", tags=["Health"])
def root():
    return {
        "service": "CareerCraft API",
        "status": "running",
        "docs": "/docs",
        "modules": ["user-profiles", "skill-gap", "semantic-search", "rag-advisory"],
    }


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
