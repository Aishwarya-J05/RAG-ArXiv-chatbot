import os
import pickle
import numpy as np
import faiss
from langchain_core.documents import Document


def build_vector_store(chunks: list, embeddings: list) -> tuple:
    """
    Build a FAISS index from chunks and their embeddings.
    
    Args:
        chunks: List of Document objects (text + metadata)
        embeddings: List of embedding vectors (one per chunk)
        
    Returns:
        Tuple of (faiss_index, chunks_list)
    """
    # Convert embeddings to numpy array (FAISS requires this)
    vectors = np.array(embeddings, dtype=np.float32)
    
    # Get dimension from first vector
    dimension = vectors.shape[1]
    print(f"📐 Vector dimensions: {dimension}")
    
    # Create FAISS index — L2 distance (Euclidean)
    index = faiss.IndexFlatL2(dimension)
    
    # Add all vectors to the index
    index.add(vectors)
    print(f"🗄️ FAISS index built with {index.ntotal} vectors")
    
    return index, chunks


def save_vector_store(index, chunks: list, path: str = "vector_store"):
    """
    Save FAISS index and chunks to disk.
    """
    os.makedirs(path, exist_ok=True)
    
    # Save FAISS index
    faiss.write_index(index, f"{path}/index.faiss")
    
    # Save chunks (your dict of text + metadata)
    with open(f"{path}/chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)
    
    print(f"💾 Saved vector store to '{path}/'")


def load_vector_store(path: str = "vector_store") -> tuple:
    """
    Load FAISS index and chunks from disk.
    """
    index = faiss.read_index(f"{path}/index.faiss")
    
    with open(f"{path}/chunks.pkl", "rb") as f:
        chunks = pickle.load(f)
    
    print(f"✅ Loaded vector store: {index.ntotal} vectors")
    return index, chunks


def search(query_embedding: list, index, chunks: list, top_k: int = 4) -> list:
    """
    Find the top_k most similar chunks to a query embedding.
    
    Args:
        query_embedding: The embedded query vector
        index: FAISS index
        chunks: List of Document objects
        top_k: Number of results to return
        
    Returns:
        List of most relevant Document objects
    """
    # Convert to numpy array
    query_vector = np.array([query_embedding], dtype=np.float32)
    
    # Search FAISS — returns distances and indices
    distances, indices = index.search(query_vector, top_k)
    
    # Map indices back to chunks (your dict lookup)
    results = []
    for i, idx in enumerate(indices[0]):
        if idx != -1:  # -1 means no result found
            chunk = chunks[idx]
            results.append({
                "text": chunk.page_content,
                "source": chunk.metadata.get("source", "unknown"),
                "page": chunk.metadata.get("page", 0),
                "distance": float(distances[0][i])
            })
    
    return results
