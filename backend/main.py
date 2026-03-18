import os
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from rag.pipeline import ingest_pdfs, ask

load_dotenv()

app = FastAPI(title="RAG ArXiv Chatbot")

# Allow React frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],  # Vite default port
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store index in memory
index = None
chunks_store = None
uploaded_files = []

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {"status": "RAG backend is running"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload a PDF and ingest it into the vector store."""
    global index, chunks_store, uploaded_files

    # Save uploaded file
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    uploaded_files.append(file_path)

    # Delete old vector store to re-embed with new file
    if os.path.exists("vector_store"):
        shutil.rmtree("vector_store")

    # Re-ingest all PDFs
    index, chunks_store = ingest_pdfs(uploaded_files)

    return JSONResponse({
        "message": f"✅ {file.filename} uploaded and indexed successfully",
        "total_files": len(uploaded_files),
        "files": [os.path.basename(f) for f in uploaded_files]
    })


@app.post("/ask")
async def ask_question(request: QuestionRequest):
    """Ask a question against the uploaded PDFs."""
    global index, chunks_store

    if index is None:
        return JSONResponse(
            status_code=400,
            content={"error": "No PDFs uploaded yet. Please upload papers first."}
        )

    result = ask(request.question, index, chunks_store)

    return JSONResponse({
        "answer": result["answer"],
        "sources": result["sources"]
    })


@app.get("/files")
def list_files():
    """List all uploaded files."""
    return {
        "files": [os.path.basename(f) for f in uploaded_files]
    }
