# Multi-Document RAG Chatbot

## Overview
This project presents a lightweight Retrieval-Augmented Generation (RAG) system designed for context-aware question answering over heterogeneous document sources. The system enables ingestion of multiple document types (PDF, DOCX, TXT, Web URLs, raw text), performs semantic indexing using dense vector embeddings, and generates responses grounded in retrieved contextual evidence.

The system uses:
* FAISS vector database
* HuggingFace embeddings
* FLAN-T5 language model
* LangChain RetrievalQA pipeline

## Key Features

Multi-document support (PDF, DOCX, TXT, Web Links, Raw Text)
Context-aware question answering
Automatic topic & summary detection
FAISS-based semantic search
Conversation history handling
Out-of-scope detection

## Architecture

* Document ingestion
* Text chunking (RecursiveCharacterTextSplitter)
* Embedding generation (MiniLM)
* FAISS vector indexing
* Retrieval + LLM generation (FLAN-T5)
* Post-processing for summaries/topics

## 🛠️ Tech Stack

* Python
* Streamlit (UI Layer)
* LangChain (Pipeline Orchestration)
* HuggingFace Transformers (LLM)
* FAISS (Vector Indexing)
* SentenceTransformer (Embeddings)
* PyPDF2/python-docx (Parsing)

### How to Run
git clone https://github.com/yourusername/multi-document-rag-chatbot.git
cd multi-document-rag-chatbot
pip install -r requirements.txt
streamlit run app_ui.py

## Project Goal
To build a lightweight, locally runnable document intelligence system using Retrieval-Augmented Generation.
