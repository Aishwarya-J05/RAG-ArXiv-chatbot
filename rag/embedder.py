import os
import time
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

def get_embedding_model():
    """
    Initialize and return the Gemini embedding model.
    """
    return GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )


def embed_chunks_in_batches(chunks: list, batch_size: int = 10) -> list:
    """
    Embed chunks in batches to avoid API rate limits.
    
    Args:
        chunks: List of Document objects
        batch_size: Number of chunks per API call
        
    Returns:
        List of embedding vectors
    """
    embeddings_model = get_embedding_model()
    all_embeddings = []
    total_batches = len(chunks) // batch_size + 1

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        batch_texts = [chunk.page_content for chunk in batch]
        
        batch_num = i // batch_size + 1
        print(f"🔄 Embedding batch {batch_num}/{total_batches}...")
        
        # Embed the batch
        batch_embeddings = embeddings_model.embed_documents(batch_texts)
        all_embeddings.extend(batch_embeddings)
        
        # Small delay to respect rate limits
        time.sleep(0.5)
    
    print(f"✅ Embedded {len(all_embeddings)} chunks total")
    return all_embeddings