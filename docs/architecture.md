# System Architecture

This document describes the high-level architecture of the Scientific Literature Explorer and how different components interact in the RAG pipeline.

## High-Level Overview

The system follows a modular Retrieval-Augmented Generation (RAG) architecture designed to keep each responsibility isolated and easy to reason about.

The overall flow is:

PDF → Text Chunks → Embeddings → Vector Store → Retriever → Context Compression → LLM → Answer

## Components

### 1. PDF Loader
Responsible for reading research papers in PDF format and extracting raw text.  
The extracted text is split into smaller overlapping chunks to balance retrieval accuracy and context size.

### 2. Embedding Module
Each text chunk is converted into a numerical vector representation using a sentence transformer model.  
These embeddings capture semantic meaning rather than keyword similarity.

### 3. Vector Store (FAISS)
FAISS is used to store embeddings and perform fast similarity search.  
It enables retrieval of the most relevant chunks for a given user query.

### 4. Retriever
The retriever compares the query embedding with stored vectors and selects the top-k most relevant chunks from the vector store.

### 5. Context Builder
Retrieved chunks are combined into a single contextual block that represents the most relevant parts of the document for the query.

### 6. Prompt Compression (ScaleDown)
Before sending the context to the language model, the prompt is compressed using ScaleDown.  
This reduces token usage while preserving semantic meaning, improving efficiency and cost control.

### 7. Answer Generator
The compressed prompt is passed to an OpenAI-compatible language model via OpenRouter for grounded answer generation.

This design allows flexible model selection and supports fallback handling in case of API or quota failures.

---

## System Interaction Flow

The system operates across three logical layers:

### 1. Interface Layer
A Streamlit-based web interface allows users to:

- Upload research papers
- Submit natural language questions
- View grounded answers

The UI interacts with the backend pipeline without containing business logic.

### 2. Retrieval Layer
Responsible for:

- Document ingestion
- Text chunking
- Embedding generation
- Semantic similarity search

### 3. Generation Layer
Handles:

- Context compression using ScaleDown
- Prompt delivery to the language model
- Grounded answer generation

This layered separation ensures scalability and clean abstraction between system components.

---

## Design Principles

- Modular components for easier debugging and replacement
- Clear separation of retrieval and generation logic
- Emphasis on grounding answers in source documents
- Optimized token usage through prompt compression
- Interface abstraction from core pipeline logic
