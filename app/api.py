# app/api.py

from fastapi import FastAPI
from pydantic import BaseModel

from app.ingestion.pipeline import build_documents
from app.retrieval.vectorstore import load_embeddings, build_vectorstore
from app.llm.model import load_llm
from app.rag.pipeline import build_rag_chain, ask_question

BASE = "https://www.esa.int"

app = FastAPI(title="RAG API")

# ---- Load everything at startup ----
print("🔄 Loading system...")

embeddings = load_embeddings()
llm = load_llm()

documents = build_documents(BASE, limit=10)
vectorstore = build_vectorstore(documents, embeddings)

rag_chain = build_rag_chain(llm, vectorstore)

print("✅ System ready")

# ---- Request schema ----
class QuestionRequest(BaseModel):
    question: str

# ---- Endpoint ----
@app.post("/ask")
def ask(req: QuestionRequest):
    result = ask_question(rag_chain, req.question)
    return result

@app.get("/")
def root():
    return {"message": "RAG API is running. Go to /docs"}