from chunking.models import chunking_files
import numpy as np
from rank_bm25 import BM25Okapi


def build_index(ALL_FILES_PATH: list[str]):
    print("type:", type(ALL_FILES_PATH))
    print("count:", len(ALL_FILES_PATH))
    print("first 3:", ALL_FILES_PATH[:3])

    chunks = []
    corpus: list = []
    token_from_corpus: list = []

    for path in ALL_FILES_PATH:
        result = chunking_files(path)
        print(path, "->", len(result), "chunks")
        chunks.extend(chunking_files(path))
    print(f"total chunks: {len(chunks)}")

    for obj in chunks:
        corpus.append(obj.text)
    for doc in corpus:
        if doc is None:
            continue
        token_from_corpus.append(doc.lower().split())
    if not token_from_corpus:
        raise ValueError("No documents to index")
    bm25 = BM25Okapi(token_from_corpus)
    return (bm25, chunks)


def search(question, t, k):

    bm25, chunks = t
    token_from_question = question.lower().split()
    score =  bm25.get_scores(token_from_question)
    top_idx = np.argsort(score)[::-1][:k]

    result = []
    for i in top_idx:
        if score[i] <= 0:
            continue
        result.append(chunks[i])
    return result

