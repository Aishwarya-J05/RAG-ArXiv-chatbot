import os
import time
import arxiv
import requests
from rag.pdf_parser import load_and_chunk_pdf

DOWNLOAD_DIR = "arxiv_papers"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Pre-load these famous papers on startup
PRELOADED_PAPERS = [
    "2106.09685",  # LoRA
    "1706.03762",  # Attention Is All You Need
]


def download_arxiv_paper(arxiv_id: str) -> str:
    """
    Download an ArXiv paper PDF by ID.
    Returns the local file path.
    """
    file_path = f"{DOWNLOAD_DIR}/{arxiv_id}.pdf"

    # Skip if already downloaded
    if os.path.exists(file_path):
        print(f"✅ Already downloaded: {arxiv_id}")
        return file_path

    print(f"📥 Downloading ArXiv paper: {arxiv_id}...")
    try:
        search = arxiv.Search(id_list=[arxiv_id])
        paper = next(arxiv.Client().results(search))
        paper.download_pdf(dirpath=DOWNLOAD_DIR, filename=f"{arxiv_id}.pdf")
        print(f"✅ Downloaded: {paper.title}")
        time.sleep(1)  # Be polite to ArXiv
        return file_path
    except Exception as e:
        print(f"❌ Failed to download {arxiv_id}: {e}")
        return None


def search_and_fetch_arxiv(query: str, max_results: int = 2) -> list:
    """
    Search ArXiv for papers matching a query.
    Downloads and chunks the top results.
    Returns list of chunks.
    """
    print(f"🔍 Searching ArXiv for: '{query}'...")
    try:
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        all_chunks = []
        for paper in arxiv.Client().results(search):
            arxiv_id = paper.entry_id.split("/")[-1]
            file_path = download_arxiv_paper(arxiv_id)
            if file_path:
                chunks = load_and_chunk_pdf(file_path)
                all_chunks.extend(chunks)
                print(f"📄 Fetched: {paper.title[:60]}...")

        print(f"✅ ArXiv fetch complete: {len(all_chunks)} new chunks")
        return all_chunks
    except Exception as e:
        print(f"❌ ArXiv search failed: {e}")
        return []


def get_preloaded_chunks() -> list:
    """
    Download and chunk all pre-loaded famous papers.
    Called once on startup.
    """
    all_chunks = []
    for arxiv_id in PRELOADED_PAPERS:
        file_path = download_arxiv_paper(arxiv_id)
        if file_path:
            chunks = load_and_chunk_pdf(file_path)
            all_chunks.extend(chunks)
    print(f"✅ Pre-loaded {len(all_chunks)} chunks from {len(PRELOADED_PAPERS)} papers")
    return all_chunks