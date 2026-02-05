def get_retriever(vectorstore, k=4):
    """Returns a retriever that fetches the top-k most relevant chunks."""
    
    return vectorstore.as_retriever(search_kwargs={"k":k})