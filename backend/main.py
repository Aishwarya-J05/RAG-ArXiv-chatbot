import os
import shutil
import threading
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from rag.pipeline import initialize_pipeline, ingest_pdf, ask, get_chunks

load_dotenv()

app = FastAPI(title="RAG ArXiv Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


class QuestionRequest(BaseModel):
    question: str


def run_initialization():
    """Run in background thread so server starts immediately."""
    try:
        initialize_pipeline()
    except Exception as e:
        print(f"❌ Initialization error: {e}")


@app.on_event("startup")
async def startup_event():
    print("🚀 Server starting — pipeline initializing in background...")
    thread = threading.Thread(target=run_initialization, daemon=True)
    thread.start()


@app.get("/")
def root():
    chunks = get_chunks()
    return {
        "status": "RAG backend is running",
        "chunks_loaded": len(chunks)
    }


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload a custom PDF and add it to the index."""
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    num_chunks = ingest_pdf(file_path)

    return JSONResponse({
        "message": f"✅ {file.filename} uploaded and indexed",
        "chunks_added": num_chunks,
        "total_chunks": len(get_chunks())
    })


@app.post("/ask")
async def ask_question(request: QuestionRequest):
    """Ask a question — searches loaded papers + auto-fetches from ArXiv if needed."""
    if not request.question.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Question cannot be empty"}
        )

    # Still initializing
    if len(get_chunks()) == 0:
        return JSONResponse({
            "answer": "⏳ Still loading papers in the background. Please wait 1-2 minutes and try again.",
            "sources": []
        })

    result = ask(request.question)
    return JSONResponse({
        "answer": result["answer"],
        "sources": result["sources"]
    })


@app.get("/files")
def list_files():
    """List loaded paper sources."""
    chunks = get_chunks()
    sources = list(set([
        c.metadata.get("source", "unknown")
        for c in chunks
    ]))
    return {"files": sources, "total_chunks": len(chunks)}