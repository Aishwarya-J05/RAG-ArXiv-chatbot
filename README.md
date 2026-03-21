# 🔬 RAG ArXiv Chatbot

> A full-stack AI research assistant that answers questions grounded in ArXiv papers — with source citations, semantic search, and a glassmorphism UI.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-009688?style=flat-square&logo=fastapi)
![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react)
![Google Gemini](https://img.shields.io/badge/Gemini-2.5_Flash-4285F4?style=flat-square&logo=google)
![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-orange?style=flat-square)
![LangChain](https://img.shields.io/badge/LangChain-0.3-1C3C3C?style=flat-square)

🌐 **Live Demo:** [rag-ar-xiv-chatbot.vercel.app](https://rag-ar-xiv-chatbot.vercel.app)  
🤗 **Backend API:** [AishwaryaNJ/rag-arxiv-backend](https://huggingface.co/spaces/AishwaryaNJ/rag-arxiv-backend)

---

## 🧠 What It Does

Upload any AI research paper (PDF) and ask questions in natural language. The chatbot:

- Retrieves the most semantically relevant chunks from your papers
- Sends them to Google Gemini as grounded context
- Returns a precise answer with **exact paper and page citations**
- Never hallucinates — answers only from what's in your documents

**Example questions:**
- *"What is LoRA and what problem does it solve?"*
- *"How does RLHF work?"*
- *"What is the key idea behind the Transformer architecture?"*

---

## 🏗️ Architecture

```
User
 ↓
React Frontend (Vite + Tailwind CSS + Framer Motion)
 ↓  HTTP requests (Axios)
FastAPI Backend (Hugging Face Spaces)
 ↓
┌──────────────────────────────────────┐
│            RAG Pipeline              │
│                                      │
│  PDF → Chunks (1000 chars, 200 ovlp) │
│           ↓                          │
│  Gemini Embeddings (3072 dims)       │
│           ↓                          │
│  FAISS Index (cached to disk)        │
│           ↓                          │
│  Query → Top-4 Semantic Matches      │
│           ↓                          │
│  Prompt + Context → Gemini 2.5 Flash │
│           ↓                          │
│  Answer + Source Citations           │
└──────────────────────────────────────┘
```

### Step-by-step RAG flow

1. **Parse** — PyMuPDF extracts raw text from uploaded PDFs
2. **Chunk** — `RecursiveCharacterTextSplitter` splits into 1000-char chunks with 200-char overlap
3. **Embed** — Each chunk → 3072-dimensional vector via `gemini-embedding-001`
4. **Store** — FAISS indexes all vectors locally and caches to disk
5. **Query** — User question is embedded into the same vector space
6. **Retrieve** — FAISS finds top-4 most semantically similar chunks
7. **Generate** — Chunks + question sent to Gemini with strict grounding instructions
8. **Cite** — Answer includes exact source filename and page number

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | React 18 + Vite | UI framework |
| Styling | Tailwind CSS v3 + Custom CSS | Glassmorphism design system |
| Animations | Framer Motion | Fluid page transitions + interactions |
| HTTP | Axios | Frontend → Backend API calls |
| Backend | FastAPI + Uvicorn | Async REST API server |
| PDF Parsing | LangChain Community + PyMuPDF | Extract + structure PDF text |
| Chunking | LangChain `RecursiveCharacterTextSplitter` | Smart overlap-aware splitting |
| Embeddings | `google-genai` SDK + `gemini-embedding-001` | 3072-dim semantic vectors |
| Vector Store | FAISS (`IndexFlatL2`) | Local similarity search |
| LLM | Google Gemini 2.5 Flash | Grounded answer generation |
| Deployment | Hugging Face Spaces (Docker) + Vercel | Backend + Frontend hosting |

---

## 📁 Project Structure

```
rag-arxiv-chatbot/
├── backend/
│   ├── main.py                  # FastAPI — /upload, /ask, /files endpoints
│   ├── requirements.txt
│   ├── Dockerfile               # HF Spaces deployment
│   └── rag/
│       ├── pdf_parser.py        # PDF loading + chunking
│       ├── embedder.py          # Gemini embeddings + rate limit retry
│       ├── vector_store.py      # FAISS build, save, load, search
│       └── pipeline.py          # Full RAG chain + prompt engineering
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Landing ↔ Chat page routing
│   │   ├── index.css            # Glassmorphism + gradient animations
│   │   └── components/
│   │       ├── LandingPage.jsx  # Hero section + feature cards
│   │       ├── ChatInterface.jsx # Main chat layout
│   │       ├── FileUpload.jsx   # Drag & drop PDF uploader
│   │       └── MessageBubble.jsx # Message with source citations
│   ├── package.json
│   └── vite.config.js
└── README.md
```

---

## 🚀 Local Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- Google Gemini API key → [Get one free](https://aistudio.google.com/apikey)

### 1. Clone the repo

```bash
git clone https://github.com/Aishwarya-J05/RAG-ArXiv-chatbot.git
cd RAG-ArXiv-chatbot
```

### 2. Backend setup

```bash
cd backend

# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
# source venv/bin/activate

pip install -r requirements.txt
```

Create `backend/.env`:
```env
GEMINI_API_KEY=your_api_key_here
```

Start backend:
```bash
uvicorn main:app --reload
# API runs at http://localhost:8000
# Auto docs at http://localhost:8000/docs
```

### 3. Frontend setup

```bash
cd ../frontend
npm install
npm run dev
# Runs at http://localhost:5173
```

### 4. Use it

1. Open `http://localhost:5173`
2. Click **"Start Researching"**
3. Upload any ArXiv paper PDF
4. Ask questions and get cited answers!

---

## 📄 Papers To Try

| Paper | Topic | PDF |
|---|---|---|
| LoRA | Parameter-efficient fine-tuning | [arxiv.org/pdf/2106.09685](https://arxiv.org/pdf/2106.09685) |
| Attention Is All You Need | Transformer architecture | [arxiv.org/pdf/1706.03762](https://arxiv.org/pdf/1706.03762) |
| InstructGPT | RLHF — how ChatGPT was trained | [arxiv.org/pdf/2203.02155](https://arxiv.org/pdf/2203.02155) |
| BERT | Bidirectional language models | [arxiv.org/pdf/1810.04805](https://arxiv.org/pdf/1810.04805) |

---

## 🔑 Key Engineering Decisions

**Why call `google-genai` SDK directly instead of LangChain's wrapper?**
`langchain-google-genai 4.x` had a bug routing embedding calls to the `v1beta` API endpoint, causing 404 errors on all models. Bypassing the wrapper and calling the SDK directly gave full control over API versioning.

**Why chunk with overlap?**
Concepts don't respect arbitrary character boundaries. A 200-character overlap ensures ideas split across two chunks are represented fully in at least one — preventing broken context from reaching the retrieval step.

**Why cache embeddings to disk?**
Embedding 111 chunks takes ~2 minutes and consumes API quota. Saving `index.faiss` + `chunks.pkl` to disk means subsequent restarts load in under a second with zero API calls.

**Why retry on 429 with backoff?**
Gemini's free tier allows 100 embedding requests/minute. A 26-page paper generates ~111 chunks — enough to hit the limit. Exponential backoff retry makes large papers work reliably without manual intervention.

**Why FAISS `IndexFlatL2` over approximate methods?**
For under 10,000 chunks, brute-force L2 search is fast enough (<10ms per query). Approximate indexes trade accuracy for speed — unnecessary at this scale and harder to reason about.

**Why FastAPI over Flask?**
Async endpoints, automatic OpenAPI docs at `/docs`, Pydantic validation, and native file upload support — all with less boilerplate.

---

## 🌐 Deployment

### Backend → Hugging Face Spaces (Docker)

```bash
cd backend
git remote add space https://huggingface.co/spaces/AishwaryaNJ/rag-arxiv-backend
git push space main
```

Add `GEMINI_API_KEY` in Space → Settings → Variables and Secrets.

### Frontend → Vercel

- Import repo at [vercel.com/new](https://vercel.com/new)
- Set root directory to `frontend`
- Add environment variable:
  ```
  VITE_API_URL = https://aishwaryanJ-rag-arxiv-backend.hf.space
  ```

---

## 🧩 What I Learned

- **RAG end-to-end** — chunking strategy, vector similarity, prompt grounding, citation extraction
- **LangChain** — document loaders, text splitters, when abstractions break and how to bypass them
- **FAISS** — how vector indexes work, L2 vs cosine distance, serialization
- **FastAPI** — async Python, CORS, file uploads, startup lifecycle events
- **React** — component architecture, useState/useRef/useEffect, Axios, Framer Motion
- **Production debugging** — SDK version mismatches, rate limiting, CORS, Docker on HF Spaces

---

## 📜 License

MIT — feel free to fork and build your own RAG projects.

---

<p align="center">
  Built from scratch by <a href="https://github.com/Aishwarya-J05">Aishwarya Joshi</a>
  <br/>
  <a href="https://rag-ar-xiv-chatbot.vercel.app">Live Demo</a> ·
  <a href="https://huggingface.co/spaces/AishwaryaNJ/rag-arxiv-backend">Backend API</a>
</p>
