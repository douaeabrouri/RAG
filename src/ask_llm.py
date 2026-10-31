from constants import MODEL_NAME, CLIENT, K, EXIT_FILES, BASE_DIR, FILE1
from src.minimalsource import MinimalSource, MinimalAnswer, MinimalSearchResults
from src.build_context import build_context
import re


def to_source(top_chunks) -> list[MinimalAnswer]:
    return [
        MinimalSource(
            file_path = str(c.file_path),
            first_char_index = str(c.first_char_index),
            last_char_index = str(c.last_char_index),
        )
        for c in top_chunks
    ]

def make_prompt(question, top_chunks) -> str:
    context = build_context(top_chunks)
    return (
        "Answer in 1 to 3 sentences using only the context below. "
        "If the answer is not in the context, say you don't know.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question} /no_think"
    )

def ask_llm(question, chunks) -> str:
    response = CLIENT.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": make_prompt(question, chunks)}],
        options={"temperature": 0},
    )
    answer = response.message.content or ""
    return re.sub(r"<think>.*?</think>", "", answer, flags=re.DOTALL).strip()