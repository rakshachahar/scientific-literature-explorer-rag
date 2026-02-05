from langchain_community.vectorstores import FAISS

def create_faiss_index(chunks, embedding_model):
    """Stores embedded document chunks in a FAISS vector store."""
    return FAISS.from_documents(chunks, embedding_model)