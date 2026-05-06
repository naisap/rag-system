# app/main.py

from app.ingestion.pipeline import build_documents
from app.retrieval.vectorstore import load_embeddings, build_vectorstore
from app.llm.model import load_llm
from app.rag.pipeline import build_rag_chain, ask_question

BASE = "https://www.esa.int"

def main():
    print("🔄 Loading system...")

    embeddings = load_embeddings()
    llm = load_llm()

    documents = build_documents(BASE, limit=10)
    vectorstore = build_vectorstore(documents, embeddings)

    rag_chain = build_rag_chain(llm, vectorstore)

    while True:
        q = input("\nAsk a question (or 'exit'): ")
        if q.lower() == "exit":
            break

        result = ask_question(rag_chain, q)
        print("\n💬", result["answer"])

if __name__ == "__main__":
    main()