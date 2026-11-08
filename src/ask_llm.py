from constants import MODEL_NAME, CLIENT, K, EXIT_FILES, BASE_DIR, FILE1
from src.minimalsource import MinimalSource, MinimalAnswer, MinimalSearchResults
from src.build_context import build_context
import re


def to_source(top_chunks) -> list[MinimalAnswer]:
    return [
        MinimalSource(
            file_path = str(c.file_path),
            first_character_index = c.first_character_index,
            last_character_index = c.last_character_index,
        )
        for c in top_chunks
    ]

def make_prompt(question, top_chunks) -> str:
    context = build_context(top_chunks)
    return (
        "You are an assistant that answers questions about the vLLM project, "
        "using only the context below. The context contains documentation and "
        "source code, each block labeled with its file path.\n\n"
        "Rules:\n"
        "- Answer in 1 to 3 sentences.\n"
        "- Copy identifiers exactly as written in the context: endpoint paths, "
        "function names, class names, parameter names, environment variables.\n"
        "- If the context contains part of the answer, give that part. "
        "Say you don't know only if the context has nothing relevant.\n"
        "- Don't use knowledge from outside the context.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n"
        "Answer:"
    )

def ask_llm(question, chunks) -> str:
    response = CLIENT.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": make_prompt(question, chunks)}],
        options={"temperature": 0},
    )
    answer = response.message.content or ""
    return re.sub(r"<think>.*?</think>", "", answer, flags=re.DOTALL).strip()