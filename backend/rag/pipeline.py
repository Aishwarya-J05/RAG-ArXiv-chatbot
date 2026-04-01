import os
import shutil
import numpy as np
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
from rag.arxiv_fetcher import get_preloaded_chunks, search_and_fetch_arxiv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options={"api_version": "v1beta"}
)

VECTOR_STORE_PATH = "vector_store"
LLM_MODEL = "gemini-2.5-flash"

# Global state
_index = None
_chunks_store = []


def get_index():
    return _index

def get_chunks():
    return _chunks_store


def initialize_pipeline():
    """
    Load vector store from disk.
    Never re-embeds — vector store is pre-built and committed to repo.
    """
    global _index, _chunks_store

    if os.path.exists(f"{VECTOR_STORE_PATH}/index.faiss"):
        print("✅ Loading pre-built vector store from disk...")
        _index, _chunks_store = load_vector_store(VECTOR_STORE_PATH)
        print(f"✅ Ready — {len(_chunks_store)} chunks loaded instantly")
        return

    # Fallback: only runs if vector store is missing (should never happen)
    print("⚠️ No vector store found — building from scratch (one-time only)...")
    chunks = get_preloaded_chunks()
    if chunks:
        embeddings = embed_chunks_in_batches(chunks)
        _index, _chunks_store = build_vector_store(chunks, embeddings)
        save_vector_store(_index, _chunks_store, VECTOR_STORE_PATH)
        print(f"✅ Built and saved — {len(_chunks_store)} chunks")


def add_to_index(new_chunks: list):
    """
    Add new chunks to existing FAISS index.
    Used when user uploads a PDF or ArXiv fetches new papers.
    """
    global _index, _chunks_store

    if not new_chunks:
        return

    print(f"➕ Adding {len(new_chunks)} new chunks to index...")
    new_embeddings = embed_chunks_in_batches(new_chunks)
    new_vectors = np.array(new_embeddings, dtype=np.float32)

    if _index is None:
        _index, _chunks_store = build_vector_store(new_chunks, new_embeddings)
    else:
        _index.add(new_vectors)
        _chunks_store.extend(new_chunks)

    save_vector_store(_index, _chunks_store, VECTOR_STORE_PATH)
    print(f"✅ Index now has {len(_chunks_store)} total chunks")


def ingest_pdf(pdf_path: str):
    """Ingest a user-uploaded PDF into the index."""
    chunks = load_and_chunk_pdf(pdf_path)
    add_to_index(chunks)
    return len(chunks)


def build_prompt(question: str, context_chunks: list) -> str:
    context = ""
    for i, chunk in enumerate(context_chunks):
        context += f"""
[Source {i+1}: {chunk['source']}, Page {chunk['page']+1}]
{chunk['text']}
---"""

    prompt = f"""You are an expert AI research assistant specializing in machine learning and AI papers.
Answer the question using ONLY the context provided below.
If the answer is not in the context, say "I don't have enough information in the provided papers to answer this."
Always cite your sources using the format: (Source: filename, Page X)

FORMAT RULES — always follow these:
- Use **bold** for key terms and important concepts
- Use bullet points starting with * for lists of features, comparisons, or properties
- Use numbered lists (1. 2. 3.) for sequential steps or ordered processes
- Use ## for section headings if the answer has multiple distinct parts
- Write in short focused paragraphs — never one long unbroken block of text
- Use `backticks` for technical terms, model names, or parameter names

CONTEXT:
{context}

QUESTION: {question}

ANSWER:"""
    return prompt


def ask(question: str, auto_fetch: bool = True) -> dict:
    """
    Full RAG pipeline:
    1. Search existing FAISS index
    2. If results are poor, auto-fetch from ArXiv
    3. Generate grounded answer
    """
    global _index, _chunks_store

    # If index is empty, try fetching from ArXiv
    if _index is None or len(_chunks_store) == 0:
        if auto_fetch:
            print("📭 Index empty — fetching from ArXiv...")
            new_chunks = search_and_fetch_arxiv(question)
            add_to_index(new_chunks)
        else:
            return {
                "answer": "No papers loaded yet. Please upload a PDF or ask a question to trigger ArXiv search.",
                "sources": []
            }

    # Search existing index
    query_embedding = get_embedding(question)
    results = search(query_embedding, _index, _chunks_store, top_k=4)

    # Check if results are confident enough (distance < 1.5)
    best_distance = results[0]['distance'] if results else 999
    print(f"🎯 Best match distance: {best_distance:.4f}")

    if best_distance > 1.2 and auto_fetch:
        print("🔍 Low confidence — fetching more papers from ArXiv...")
        new_chunks = search_and_fetch_arxiv(question, max_results=2)
        if new_chunks:
            add_to_index(new_chunks)
            # Re-search with expanded index
            results = search(query_embedding, _index, _chunks_store, top_k=4)

    # Generate answer
    prompt = build_prompt(question, results)
    response = client.models.generate_content(
        model=LLM_MODEL,
        contents=prompt
    )

    sources = list(set([
        f"{c['source']} (Page {c['page']+1})"
        for c in results
    ]))

    return {
        "answer": response.text,
        "sources": sources
    }