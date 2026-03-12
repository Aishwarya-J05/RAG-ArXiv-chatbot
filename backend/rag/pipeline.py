import os
from dotenv import load_dotenv
from google import genai
from rag.pdf_parser import load_and_chunk_pdf
from rag.embedder import embed_chunks_in_batches, get_embedding
from rag.vector_store import (
    build_vector_store,
    save_vector_store,
    load_vector_store,
    search
)

load_dotenv()

# Gemini client for generation
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options={"api_version": "v1beta"}
)

VECTOR_STORE_PATH = "vector_store"
LLM_MODEL = "gemini-2.5-flash"


def ingest_pdfs(pdf_paths: list):
    """
    Parse, chunk, embed and store PDFs into FAISS.
    Skips re-embedding if vector store already exists.
    
    Args:
        pdf_paths: List of paths to PDF files
    """
    # Check cache — if already embedded, skip
    if os.path.exists(f"{VECTOR_STORE_PATH}/index.faiss"):
        print("✅ Vector store already exists. Loading from disk...")
        return load_vector_store(VECTOR_STORE_PATH)

    print("🔄 No cache found. Embedding PDFs from scratch...")
    
    all_chunks = []
    
    # Load and chunk all PDFs
    for pdf_path in pdf_paths:
        chunks = load_and_chunk_pdf(pdf_path)
        all_chunks.extend(chunks)
    
    print(f"📚 Total chunks across all PDFs: {len(all_chunks)}")
    
    # Embed all chunks
    embeddings = embed_chunks_in_batches(all_chunks)
    
    # Build and save FAISS index
    index, chunks_store = build_vector_store(all_chunks, embeddings)
    save_vector_store(index, chunks_store, VECTOR_STORE_PATH)
    
    return index, chunks_store


def build_prompt(question: str, context_chunks: list) -> str:
    """
    Build the RAG prompt with retrieved context.
    
    Args:
        question: User's question
        context_chunks: Retrieved chunks from FAISS
        
    Returns:
        Complete prompt string for Gemini
    """
    context = ""
    for i, chunk in enumerate(context_chunks):
        context += f"""
[Source {i+1}: {chunk['source']}, Page {chunk['page']+1}]
{chunk['text']}
---"""

    prompt = f"""You are an expert AI research assistant.
Answer the question using ONLY the context provided below.
If the answer is not in the context, say "I don't have enough information in the provided papers to answer this."
Always cite your sources using the format: (Source: filename, Page X)

CONTEXT:
{context}

QUESTION: {question}

ANSWER:"""
    
    return prompt


def ask(question: str, index, chunks_store: list) -> dict:
    """
    Full RAG pipeline: embed question → search → generate answer.
    
    Args:
        question: User's question
        index: FAISS index
        chunks_store: List of chunks
        
    Returns:
        Dict with answer and sources
    """
    # Step 1: Embed the question
    query_embedding = get_embedding(question)
    
    # Step 2: Retrieve relevant chunks
    relevant_chunks = search(query_embedding, index, chunks_store, top_k=4)
    
    # Step 3: Build prompt
    prompt = build_prompt(question, relevant_chunks)
    
    # Step 4: Generate answer with Gemini
    response = client.models.generate_content(
        model=LLM_MODEL,
        contents=prompt
    )
    
    # Step 5: Extract sources for citation
    sources = list(set([
        f"{c['source']} (Page {c['page']+1})" 
        for c in relevant_chunks
    ]))
    
    return {
        "answer": response.text,
        "sources": sources
    }