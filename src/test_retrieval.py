from loaders.pdf_loader import load_and_split_pdf
from embeddings.embedder import get_embedding_model
from vectorstore.faiss_store import create_faiss_index
from rag.retriever import get_retriever

pdf_path = "data/sample_papers/research_paper.pdf"

print("Loading and chunking PDF...")
chunks = load_and_split_pdf(pdf_path)
print(f"Total chunks:{len(chunks)}")

print("Creating embeddings...")
embedding_model = get_embedding_model()

print("Building FAISS index...")
vectorstore = create_faiss_index(chunks, embedding_model)

retriever = get_retriever(vectorstore)

query = "What is the main focus of this research paper?"
print(f"\nQuery:{query}\n")

docs = retriever.invoke(query)

for i, doc in enumerate(docs,1):
    print(f"---Retrieved chunk {i}---")
    print(doc.page_content[:300])
    print()