# Scientific Literature Explorer — Research Paper Q&A using RAG

An end-to-end Retrieval-Augmented Generation (RAG) system that allows users to query research papers in plain English and receive answers grounded directly in the source document.

## Problem Statement

Academic research papers are often long, dense, and time-consuming to read. Finding specific information usually requires manually scanning dozens of pages or relying on keyword search, which often misses the actual meaning of the text.

While large language models can answer questions quickly, they tend to hallucinate when they are not grounded in the source material. This makes them unreliable for serious research use without proper context.

The challenge is to build a system that can understand the content of a research paper, retrieve the most relevant sections for a given question, and generate answers that are directly grounded in the paper itself.

## Solution Overview

To address this problem, this project implements a Retrieval-Augmented Generation (RAG) pipeline that enables users to interact with research papers through natural language questions.

The system begins by ingesting a research paper in PDF format and converting it into machine-readable text. This text is then split into smaller chunks to make it easier to process and retrieve relevant information.

Each chunk is transformed into vector embeddings and stored in a FAISS vector database. When a user asks a question, the system performs semantic search to retrieve the most relevant sections of the paper.

The retrieved context is then compressed using ScaleDown to optimize prompt size and reduce token usage before being sent to the language model. Finally, the LLM generates an answer grounded in the retrieved content, ensuring that responses remain relevant to the source document.

## Project Architecture

The system is structured as a modular pipeline, where each component has a clear responsibility.

- **PDF Loader**  
  Extracts text from research papers and splits it into manageable chunks.

- **Embedding Module**  
  Converts text chunks into vector embeddings using a sentence transformer model.

- **Vector Store (FAISS)**  
  Stores embeddings and enables fast semantic similarity search.

- **Retriever**  
  Fetches the most relevant chunks from the vector store based on a user query.

- **Context Builder**  
  Combines retrieved chunks into a single contextual input for the language model.

- **Prompt Compression (ScaleDown)**  
  Compresses the context and question to reduce token usage while preserving meaning.

- **Answer Generator**  
  Uses a language model to generate answers grounded in the retrieved document context.

This modular design makes the system easier to debug, extend, and replace individual components as needed.

## Tech Stack

- **Python** – Core programming language  
- **LangChain** – Orchestrating the RAG pipeline  
- **FAISS** – Vector database for semantic search  
- **Sentence Transformers** – Generating text embeddings  
- **ScaleDown API** – Prompt compression and token optimization  
- **Google Gemini / OpenAI-compatible LLMs** – Answer generation

## Project Status

This project currently supports question answering over a single research paper PDF using a command-line interface.

Future improvements may include:
- Multi-document support
- Web-based UI
- Citation highlighting in answers
- Persistent vector storage

The current focus is on correctness, clarity, and understanding the core RAG workflow.

## Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/rakshachahar/scientific-literature-explorer-rag.git
cd scientific-literature-explorer-rag
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set required API keys

```bash
export SCALEDOWN_API_KEY="your_scaledown_key_here"
export GEMINI_API_KEY="your_gemini_key_here"
```

### 4. Add a research paper

Place a PDF file inside:

```
data/sample_papers/
```

### 5. Run the application

```bash
python src/app.py
```

## Example Usage

**Question**

```
What is the main focus of this research paper?
```

**Generated Answer**

The study examines how advanced language learners use mobile devices to support English language learning, based on interview-based qualitative analysis.

## Project Structure

```text
src/
├── loaders/        # PDF ingestion & chunking
├── embeddings/     # Embedding generation
├── vectorstore/    # FAISS indexing
├── rag/            # Retrieval + generation pipeline
└── app.py          # CLI entry point

data/
└── sample_papers/  # Input research papers
```