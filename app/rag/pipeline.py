# app/rag/pipeline.py

from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import PromptTemplate

def build_rag_chain(llm, vectorstore):
    prompt_template = """You are a helpful assistant.

Answer the question using ONLY the context below.
If the answer is not in the articles, say "I don't have information about that."
Always mention which article your answer comes from.
Keep your answer concise.

Context:
{context}

Question:
{input}

Answer:"""

    prompt = PromptTemplate.from_template(prompt_template)

    qa_chain = create_retrieval_chain(
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        combine_docs_chain=create_stuff_documents_chain(llm, prompt)
    )

    return qa_chain

def ask_question(chain, question):
    result = chain.invoke({"input": question})

    sources = []
    for doc in result.get("context", []):
        sources.append({
            "title": doc.metadata.get("title"),
            "source": doc.metadata.get("source")
        })

    return {
        "answer": result["answer"],
        "sources": sources
    }