from rag.pipeline import ingest_pdfs, ask

# Ingest (will load from cache since we already saved)
index, chunks_store = ingest_pdfs(["lora.pdf"])

# Ask a question
result = ask("What is LoRA and what problem does it solve?", index, chunks_store)

print("\n💬 Answer:")
print(result["answer"])

print("\n📚 Sources:")
for source in result["sources"]:
    print(f"  → {source}")