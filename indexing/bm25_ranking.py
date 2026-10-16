from chunking.chunker import get_files_path, PATH
from chunking.models import chunking_files
import numpy as np
from rank_bm25 import BM25Okapi
from collections import Counter


def build_index(ALL_FILES_PATH: list[str]):

    chunks = []
    corpus: list = []
    token_from_corpus: list = []

    for path in ALL_FILES_PATH:
        chunks.extend(chunking_files(path))

    for obj in chunks:
        corpus.append(obj.text)

    for doc in corpus:
        if doc is None:
            continue
        token_from_corpus.append(doc.lower().split())

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
        chunk = chunks[i]
        result.append((chunk.file_path, chunk.first_char_index, chunk.last_char_index))
    return result

