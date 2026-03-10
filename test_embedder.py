from rag.pdf_parser import load_and_chunk_pdf
from rag.embedder import embed_chunks_in_batches

chunks = load_and_chunk_pdf('lora.pdf')
embeddings = embed_chunks_in_batches(chunks[:5])

print(f'Vector length: {len(embeddings[0])}')
print(f'First 5 values: {embeddings[0][:5]}')