from rag.pdf_parser import load_and_chunk_pdf
from rag.embedder import embed_chunks_in_batches, get_embedding
from rag.vector_store import build_vector_store, save_vector_store, search

# Load and embed
chunks = load_and_chunk_pdf('lora.pdf')
embeddings = embed_chunks_in_batches(chunks[:20])  # test with 20 chunks

# Build vector store
index, chunks_store = build_vector_store(chunks[:20], embeddings)

# Save it
save_vector_store(index, chunks_store)

# Test search
query = "What is LoRA and how does it work?"
query_embedding = get_embedding(query)
results = search(query_embedding, index, chunks_store, top_k=3)

print("\n🔍 Search Results:")
for i, r in enumerate(results):
    print(f"\n--- Result {i+1} ---")
    print(f"Source: {r['source']}, Page: {r['page']}")
    print(f"Distance: {r['distance']:.4f}")
    print(f"Text: {r['text'][:200]}...")