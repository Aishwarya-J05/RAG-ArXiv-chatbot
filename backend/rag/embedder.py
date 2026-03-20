import os
import time
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options={"api_version": "v1beta"}
)

EMBEDDING_MODEL = "gemini-embedding-001"


def get_embedding(text: str) -> list:
    """Embed text with automatic retry on rate limit."""
    max_retries = 5
    for attempt in range(max_retries):
        try:
            result = client.models.embed_content(
                model=EMBEDDING_MODEL,
                contents=text
            )
            return result.embeddings[0].values
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                wait = 30 + (attempt * 10)  # 30s, 40s, 50s...
                print(f"⏳ Rate limit hit. Waiting {wait}s before retry...")
                time.sleep(wait)
            else:
                raise e
    raise Exception("Max retries exceeded for embedding")


def embed_chunks_in_batches(chunks: list, batch_size: int = 5) -> list:
    """Embed all chunks with rate limit handling."""
    all_embeddings = []
    total = len(chunks)

    for i, chunk in enumerate(chunks):
        print(f"🔄 Embedding chunk {i+1}/{total}...")
        embedding = get_embedding(chunk.page_content)
        all_embeddings.append(embedding)

        # Pause every batch to stay under 100/min
        if (i + 1) % batch_size == 0:
            time.sleep(3)  # 5 chunks per 3s = ~100/min max

    print(f"✅ Embedded {len(all_embeddings)} chunks total")
    return all_embeddings