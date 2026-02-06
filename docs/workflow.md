# Application Workflow

This document explains how the system behaves at runtime when a user interacts with the application.

## Step-by-Step Flow

1. The user uploads a research paper PDF through the Streamlit interface.
2. The application temporarily stores the uploaded file.
3. The PDF is loaded and text content is extracted.
4. Extracted text is split into overlapping chunks.
5. Each chunk is embedded into a vector representation.
6. All embeddings are indexed using FAISS.
7. The user enters a natural language question in the UI.
8. The question is embedded and compared against stored vectors.
9. The retriever selects the most relevant chunks.
10. Retrieved chunks are merged into a single context.
11. The context and question are compressed using ScaleDown.
12. The compressed prompt is sent to the language model.
13. The model generates a response grounded in the document content.
14. The generated answer is displayed in the UI.

---

## LLM Failure Handling

If answer generation fails due to API limits, quota exhaustion, or network issues:

- The system falls back to displaying retrieved document context.
- This ensures the user still receives relevant information.
- The fallback maintains system usability even without active LLM access.

---

## Error Handling Considerations

- Missing PDFs are handled via upload validation.
- Empty questions trigger user warnings.
- API failures are surfaced with fallback responses.
- Modular design allows independent component debugging.

---

## Current Limitations

- Supports a single PDF at a time
- Uses in-memory vector storage
- No persistent indexing
- Limited citation highlighting

These limitations are intentional to maintain focus on core RAG pipeline understanding.
