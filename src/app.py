from loaders.pdf_loader import load_and_split_pdf
from embeddings.embedder import get_embedding_model
from vectorstore.faiss_store import create_faiss_index
from rag.retriever import get_retriever
from rag.context_builder import build_context
from rag.scaledown_client import compress_prompt
from rag.generator import generate_answer

def main():
    print("Initializing RAG system...")

    chunks = load_and_split_pdf("data/sample_papers/research_paper.pdf")
    embeddings = get_embedding_model()
    vectorstore = create_faiss_index(chunks, embeddings)
    retriever = get_retriever(vectorstore)

    while True:
        question = input("\nAsk a question (type 'exit' to quit): ")
        if question.lower() == "exit":
            break

        docs = retriever.invoke(question)
        context = build_context(docs)

        compressed_prompt = compress_prompt(context, question)
        answer = generate_answer(compressed_prompt)

        print("\nAnswer:\n", answer)


if __name__ == "__main__":
    main()
