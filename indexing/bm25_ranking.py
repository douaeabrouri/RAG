from chunking.chunker import get_files_path, PATH
from chunking.models import chunking_files
from pathlib import Path
from rank_bm25 import BM25Okapi

ALL_FILES_PATH: list[str] = []
ALL_FILES_PATH = get_files_path(PATH)

PATH_TEST = Path("/Users/ameen/Desktop/RAG/vllm_tester/file.py")

def build_index(PATH_TEST) -> tuple:

    chunks = chunking_files(PATH_TEST)
    corpus: list = []
    token_from_corpus: list = []

    corpus = [corpus.append(obj.text) for obj in chunks]
    for doc in corpus:
        token_from_corpus.append(doc.lower().split())

    bm25 = BM25Okapi(token_from_corpus)
    return (bm25, chunks)

def search():
    ...




