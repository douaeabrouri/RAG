import pickle
from src.chunking.models import chunking_files
import numpy as np
from rank_bm25 import BM25Okapi
import re
from src.constants import DEFAULT_MAX_CHUNK_SIZE
from pathlib import Path
from tqdm import tqdm


def tokenize(text: str) -> list[str]:
    """Normalize source text into lowercase alphanumeric search tokens.

    Args:
        text: Text to tokenize.

    Returns:
        Lowercase alphabetic and numeric tokens.
    """
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text)
    return re.findall(r"[a-z]+|[0-9]+", text.lower())


def build_index(
    ALL_FILES_PATH: list[str],
    max_chunk_size: int = DEFAULT_MAX_CHUNK_SIZE,
):
    """Chunk files and build a BM25 index over their text.

    Args:
        ALL_FILES_PATH: Paths of supported files to include in the index.
        max_chunk_size: Maximum number of characters per generated chunk.

    Returns:
        A tuple containing the BM25 index and the corresponding chunks.

    Raises:
        ZeroDivisionError: If no non-empty document tokens were produced.
    """

    chunks = []
    corpus: list = []
    token_from_corpus: list = []

    for path in tqdm(
        ALL_FILES_PATH,
        desc="Indexing files",
        unit="file"
    ):
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


def search(question, bm25, chunks, k) -> list:
    """Return up to ``k`` chunks with positive BM25 relevance scores.

    Args:
        question: Search query to rank against the indexed chunks.
        bm25: BM25 index built from the same chunk collection.
        chunks: Chunks in the same order used to build ``bm25``.
        k: Maximum number of ranked chunks to return.

    Returns:
        Relevant chunks ordered from highest to lowest score.
    """

    token_from_question = tokenize(question)
    score = bm25.get_scores(token_from_question)
    top_idx = np.argsort(score)[::-1][:k]

    result = []
    for i in top_idx:
        if score[i] <= 0:
            continue
        result.append(chunks[i])
    return result


def load_index(prossed_dir: str):
    """Load a serialized BM25 index from a processed-data directory.

    Args:
        prossed_dir: Directory expected to contain ``index.pkl``.

    Returns:
        The deserialized index object.

    Raises:
        FileNotFoundError: If the index file does not exist.
        ValueError: If the index cannot be deserialized.
    """

    PATH = Path(prossed_dir) / "index.pkl"
    if not PATH.exists():
        raise FileNotFoundError(f"ERROR: file {PATH} not found")

    try:
        with open(prossed_dir, "rb") as file:
            return (pickle.load(file))
    except Exception as e:
        raise ValueError(f"ERROR: {e}")
