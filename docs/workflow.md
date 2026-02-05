# Application Workflow

This document explains how the system behaves at runtime when a user asks a question.

## Step-by-Step Flow

1. The user places a research paper PDF inside the `data/sample_papers/` directory.
2. The application loads the PDF and extracts text content.
3. Extracted text is split into overlapping chunks.
4. Each chunk is embedded into a vector representation.
5. All embeddings are indexed using FAISS.
6. The user enters a natural language question.
7. The question is embedded and compared against stored vectors.
8. The retriever selects the most relevant chunks.
9. Retrieved chunks are merged into a single context.
10. The context and question are compressed using ScaleDown.
11. The compressed prompt is sent to the language model.
12. The model generates a response grounded in the document content.
13. The answer is returned to the user via the CLI.

## Error Handling Considerations

- Missing PDFs are handled by early validation.
- API failures are surfaced clearly during runtime.
- Modular design allows individual components to be tested independently.

## Current Limitations

- Supports a single PDF at a time
- Uses in-memory vector storage
- CLI-based interaction only

These limitations are intentional to keep the system focused on understanding core RAG concepts.
