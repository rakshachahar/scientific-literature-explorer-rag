from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_and_split_pdf(pdf_path: str):
    # Step 1 : Load PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    #Step 2 : Split text into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 800,
        chunk_overlap = 150
    )

    chunks = splitter.split_documents(documents)
    return chunks

if __name__ == "__main__":
    chunks = load_and_split_pdf("data/sample_papers/research_paper.pdf")
    print(f"Total chunks: {len(chunks)}")
    print(chunks[0].page_content[:300])

