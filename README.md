# 🔬 RAG ArXiv Chatbot

> A full-stack AI research assistant that answers questions about AI/ML papers — with automatic ArXiv search, semantic retrieval, and source citations.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-009688?style=flat-square&logo=fastapi)
![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react)
![Google Gemini](https://img.shields.io/badge/Gemini-2.5_Flash-4285F4?style=flat-square&logo=google)
![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-orange?style=flat-square)
![LangChain](https://img.shields.io/badge/LangChain-0.3-1C3C3C?style=flat-square)
![ArXiv](https://img.shields.io/badge/ArXiv-Auto_Search-B31B1B?style=flat-square)

🌐 **Live Demo:** [rag-ar-xiv-chatbot.vercel.app](https://rag-ar-xiv-chatbot.vercel.app)
🤗 **Backend API:** [AishwaryaNJ/rag-arxiv-backend](https://huggingface.co/spaces/AishwaryaNJ/rag-arxiv-backend)
📁 **GitHub:** [Aishwarya-J05/RAG-ArXiv-chatbot](https://github.com/Aishwarya-J05/RAG-ArXiv-chatbot)

---

## What It Does

Ask any question about AI/ML research in natural language. The system:

- **Auto-fetches** relevant ArXiv papers if the answer isn't already indexed
- **Pre-loads** 7 landmark AI papers on startup (Transformers, GPT-3, LLaMA, and more)
- Retrieves the most semantically relevant chunks using FAISS vector search
- Returns **structured markdown answers** with bold terms, bullet points, and headings
- Cites the **exact paper and page number** for every claim
- Optionally accepts **custom PDF uploads** alongside ArXiv search

**Example questions:**
- *"What is the Transformer architecture?"*
- *"What is LoRA and how does it work?"*
- *"What is QLoRA?"*

---

## 🏗️ Architecture

```
User asks a question
        ↓
Search existing FAISS index (pre-loaded + uploaded papers)
        ↓
If confidence low → Auto-fetch from ArXiv API
        ↓
Download PDF → Chunk → Embed → Add to FAISS
        ↓
Retrieve top-4 semantically similar chunks
        ↓
Build grounded prompt → Gemini 2.5 Flash
        ↓
Structured markdown answer + source citations
```

### RAG Pipeline — Step by Step

| Step | What Happens | File |
|---|---|---|
| **Parse** | PyMuPDF extracts text from PDF, returns Documents with metadata | `pdf_parser.py` |
| **Chunk** | `RecursiveCharacterTextSplitter` splits into 1000-char chunks, 200 overlap | `pdf_parser.py` |
| **Embed** | Each chunk → 3072-dim vector via `gemini-embedding-001` | `embedder.py` |
| **Store** | FAISS `IndexFlatL2` indexes all vectors, cached to disk | `vector_store.py` |
| **Fetch** | ArXiv API searched if confidence is low (distance > 1.2) | `arxiv_fetcher.py` |
| **Retrieve** | Top-4 closest chunks found via L2 similarity search | `vector_store.py` |
| **Generate** | Chunks + question → Gemini with strict grounding + markdown instructions | `pipeline.py` |
| **Cite** | Source filename + page returned alongside answer | `pipeline.py` |

---

## 📚 Pre-loaded Papers

These 7 landmark papers are automatically downloaded and indexed on first startup:

| Paper | Topic | ArXiv ID |
|---|---|---|
| Attention Is All You Need | Transformer architecture | 1706.03762 |
| Language Models are Few-Shot Learners | GPT-3 | 2005.14165 |
| LLaMA | Open foundation language models | 2302.13971 |
| Tree of Thoughts | Deliberate problem solving with LLMs | 2305.10601 |
| LoRA | Parameter-efficient fine-tuning | 2106.09685 |
| InstructGPT | RLHF training | 2203.02155 |
| BERT | Bidirectional language models | 1810.04805 |

> First startup takes ~5-6 minutes to embed all chunks. Subsequent startups load from cache in under 1 second.

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | React 18 + Vite | UI framework |
| Styling | Tailwind CSS v3 + Custom CSS | Glassmorphism design system |
| Animations | Framer Motion | Fluid page transitions + interactions |
| Markdown | react-markdown | Renders structured AI responses |
| HTTP | Axios | Frontend → Backend API calls |
| Backend | FastAPI + Uvicorn | Async REST API server |
| PDF Parsing | LangChain Community + PyMuPDF | Extract + structure PDF text |
| Chunking | LangChain `RecursiveCharacterTextSplitter` | Smart overlap-aware splitting |
| Embeddings | `google-genai` SDK + `gemini-embedding-001` | 3072-dim semantic vectors |
| Vector Store | FAISS (`IndexFlatL2`) | Local similarity search |
| ArXiv Search | `arxiv` Python library | Auto-fetch relevant papers |
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
│       ├── arxiv_fetcher.py     # ArXiv API search + auto-download
│       └── pipeline.py          # Full RAG chain + confidence-based fetch
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Landing ↔ Chat page routing
│   │   ├── index.css            # Glassmorphism + gradient animations
│   │   └── components/
│   │       ├── LandingPage.jsx  # Hero section + feature cards
│   │       ├── ChatInterface.jsx # Main chat + suggested questions
│   │       ├── FileUpload.jsx   # Optional drag & drop PDF uploader
│   │       └── MessageBubble.jsx # Markdown-rendered message + citations
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

pip install -r requirements.txt
```

Create `backend/.env`:
```env
GEMINI_API_KEY=your_api_key_here
```

Start backend:
```bash
uvicorn main:app --reload
# First run: downloads + embeds pre-loaded papers (~5 min)
# Subsequent runs: loads from cache instantly
# API docs at http://localhost:8000/docs
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
3. Ask any AI research question — no upload needed!
4. Optionally upload your own PDF for custom papers

---

## 🔑 Key Engineering Decisions

**Why auto-fetch from ArXiv instead of manual upload only?**
Manual upload puts friction on the user. By pre-loading famous papers and auto-fetching when confidence is low (L2 distance > 1.2), the system works out of the box for the most common AI research questions — no setup required.

**How does confidence-based fetching work?**
After the initial FAISS search, we check the L2 distance of the best result. Distance > 1.2 means the closest chunk in our index isn't very similar to the question — so we search ArXiv for relevant papers, download them, embed the chunks, add them to FAISS, and re-search. The threshold was tuned empirically.

**Why bypass LangChain's embedding wrapper?**
`langchain-google-genai 4.x` had a bug routing all embedding calls to the `v1beta` API endpoint, causing 404 errors. Calling `google-genai` SDK directly gave full control over API versioning and fixed the issue immediately.

**Why cache embeddings to disk?**
Embedding 553 chunks takes ~5 minutes and consumes significant API quota. Saving `index.faiss` + `chunks.pkl` means subsequent restarts load in under 1 second with zero API calls.

**Why render responses as markdown?**
Gemini naturally uses markdown in its responses — bold terms, bullet points, numbered lists. Without `react-markdown`, these render as raw asterisks and hyphens. Proper markdown rendering makes answers dramatically more readable and professional.

**Why `IndexFlatL2` over approximate search?**
For portfolios under 10,000 chunks, brute-force exact L2 search is fast enough (<10ms). Approximate indexes trade accuracy for speed — unnecessary at this scale.

---

## 🌐 Deployment

### Backend → Hugging Face Spaces (Docker)

```bash
cd backend
git remote add space https://huggingface.co/spaces/AishwaryaNJ/rag-arxiv-backend
git push space main
```

Add `GEMINI_API_KEY` in Space → Settings → Variables and Secrets.

> Note: First startup on HF Spaces downloads and embeds all pre-loaded papers. This takes ~5-6 minutes but only happens once.

### Frontend → Vercel

- Import repo at [vercel.com/new](https://vercel.com/new)
- Set root directory to `frontend`
- Add environment variable:
  ```
  VITE_API_URL = https://aishwaryanJ-rag-arxiv-backend.hf.space
  ```

The frontend automatically falls back to `http://localhost:8000` when `VITE_API_URL` is not set — same code works in both local and production environments.

---

## 🧩 What I Learned

- **RAG end-to-end** — chunking strategy, vector similarity, confidence-based retrieval, prompt grounding
- **LangChain** — document loaders, text splitters, when abstractions break and how to bypass them
- **FAISS** — vector indexing, L2 distance, serialization, dynamic index updates
- **ArXiv API** — programmatic paper search and download, rate limit handling
- **FastAPI** — async Python, CORS, file uploads, startup lifecycle events
- **React** — component architecture, useState/useRef/useEffect, Axios, Framer Motion
- **react-markdown** — rendering structured LLM responses with custom component styling
- **Production debugging** — SDK version mismatches, rate limiting, CORS, Docker on HF Spaces

---

## 📜 License

MIT — feel free to fork and build your own RAG projects.

---

<p align="center">
  Built from scratch by <a href="https://github.com/Aishwarya-J05">Aishwarya Joshi</a>
  <br/>
  <a href="https://rag-ar-xiv-chatbot.vercel.app">Live Demo</a> ·
  <a href="https://huggingface.co/spaces/AishwaryaNJ/rag-arxiv-backend">Backend API</a> ·
  <a href="https://github.com/Aishwarya-J05/RAG-ArXiv-chatbot">GitHub</a>
</p>
