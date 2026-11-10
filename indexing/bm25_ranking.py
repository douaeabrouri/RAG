import pickle
from chunking.models import chunking_files
import numpy as np
from rank_bm25 import BM25Okapi
import re
from constants import DEFAULT_MAX_CHUNK_SIZE


def tokenize(text: str) -> list[str]:
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text)
    return re.findall(r"[a-z]+|[0-9]+", text.lower())


def build_index(
    ALL_FILES_PATH: list[str],
    max_chunk_size: int = DEFAULT_MAX_CHUNK_SIZE,
):

    chunks = []
    corpus: list = []
    token_from_corpus: list = []

    for path in ALL_FILES_PATH:
        chunks.extend(chunking_files(path, max_chunk_size))

    for obj in chunks:
        corpus.append(obj.text)
    for doc in corpus:
        if doc is None:
            continue
        token_from_corpus.append(tokenize(doc))
    if not token_from_corpus:
        raise ZeroDivisionError("No documents to index")
    bm25 = BM25Okapi(token_from_corpus)
    return (bm25, chunks)

def search(question, bm25, chunks, k) ->list:

    token_from_question = tokenize(question)
    score =  bm25.get_scores(token_from_question)
    top_idx = np.argsort(score)[::-1][:k]

    result = []
    for i in top_idx:
        if score[i] <= 0:
            continue
        result.append(chunks[i])
    return result

def load_index(proessed_dir: str):

    PATH = proessed_dir / "index.pkl"
    if not PATH.exits():
        raise FileNotFoundError(f"ERROR: file {PATH} not found")

    try:
        with open(proessed_dir, "rb") as file:
            return (pickle.load(file))
    except Exception as e:
        raise ValueError(f"ERROR: {e}")



