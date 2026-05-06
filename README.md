# RAG System – ESA Articles QA

## Overview
This project implements a Retrieval-Augmented Generation (RAG) system
to answer questions about ESA (European Space Agency) articles.

## Architecture
- **Ingestion**: Web scraping ESA articles
- **Processing**: Text chunking
- **Retrieval**: Chroma vector database
- **LLM**: FLAN-T5 (HuggingFace)
- **Pipeline**: LangChain-based RAG

## Features
- Automatic article scraping
- Semantic search over documents
- Context-aware question answering
- Modular and scalable design

## Run locally
```bash
conda activate AI_ML
python app/main.py
