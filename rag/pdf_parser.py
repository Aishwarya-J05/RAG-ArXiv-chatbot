import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_and_chunk_pdf(pdf_path: str) -> list:
    """
    Load a PDF file and split it into chunks.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        List of Document objects with text + metadata
    """
    # Step 1: Load the PDF
    loader = PyMuPDFLoader(pdf_path)
    documents = loader.load()
    
    # Step 2: Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,       # max characters per chunk
        chunk_overlap=200,     # overlap between chunks
        separators=["\n\n", "\n", " ", ""]  # try these in order
    )
    
    chunks = splitter.split_documents(documents)
    
    print(f"✅ Loaded: {os.path.basename(pdf_path)}")
    print(f"📄 Pages: {len(documents)}")
    print(f"🧩 Chunks: {len(chunks)}")
    
    return chunks