from chunking.chunker import get_files_path, PATH
from chunking.models import chunking_files
from pathlib import Path
from rank_bm25 import BM25Okapi

ALL_FILES_PATH: list[str] = []
ALL_FILES_PATH = get_files_path(PATH)

PATH_TEST = Path("/Users/ameen/Desktop/RAG/vllm_tester/question_test.txt")


def build_index(PATH_TEST) -> tuple:

    chunks = chunking_files(PATH_TEST)
    corpus: list = []
    token_from_corpus: list = []


    for obj in chunks:
        corpus.append(obj.text)

    for doc in corpus:
        if doc is None:
            print("Found Nothing In Corpus!")
            continue
        token_from_corpus.append(doc.lower().split())

    bm25 = BM25Okapi(token_from_corpus)
    return (bm25, chunks)

question: str = "What are the default values for FP8_MIN and FP8_MAX constants in vLLM's triton_flash_attention module?"

def search(question, t):

    bm25, chunks = t
    token_from_question = question.lower().split()
    score =  bm25.get_scores(token_from_question)
    top_k = bm25.get_top_n(token_from_question, chunks, 1)
    print(top_k.text)

search(question, build_index(PATH_TEST))

