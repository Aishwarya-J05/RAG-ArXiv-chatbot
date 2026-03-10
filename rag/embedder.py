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
    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text
    )
    return result.embeddings[0].values


def embed_chunks_in_batches(chunks: list, batch_size: int = 5) -> list:
    all_embeddings = []
    total = len(chunks)

    for i, chunk in enumerate(chunks):
        print(f"🔄 Embedding chunk {i+1}/{total}...")
        
        embedding = get_embedding(chunk.page_content)
        all_embeddings.append(embedding)
        
        if (i + 1) % batch_size == 0:
            time.sleep(1)

    print(f"✅ Embedded {len(all_embeddings)} chunks total")
    return all_embeddings