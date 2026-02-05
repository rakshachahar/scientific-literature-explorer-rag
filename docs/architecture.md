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
The compressed context and user question are passed to the language model, which generates a grounded answer based only on the retrieved document content.

## Design Principles

- Modular components for easier debugging and replacement
- Separation of retrieval and generation logic
- Emphasis on grounding answers in source documents
- Optimized token usage through prompt compression
