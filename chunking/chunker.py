from pydantic import BaseModel
from chunking.markdown_chunker import chunk_markdown
from chunking.python_chunker import chunk_python
from chunking.txt_chunker import chunk_txt
from pathlib import Path

ALLOWED_FILES = [".py", ".md", ".txt"]
MAX_CHARS = 2000
PATH = Path("/Users/ameen/Desktop/RAG-douae/vllm_tester")

class MinimalSource(BaseModel) :
    id    : int
    text   : str
    file_path: str
    first_line : int
    last_line  : int 
    first_char_index: int
    last_char_index: int

def get_files_path(root: str) -> list[Path]:
    files_paths: list[Path] = []

    for file in PATH.rglob("*"):
        if not file.is_file():
            continue
        if file.suffix not in ALLOWED_FILES:
            continue
        files_paths.append(file)
    return files_paths

def chunking_file(file_path: Path):

    with open("/Users/ameen/Desktop/RAG-douae/vllm_tester/file.py", "r") as file:
        code = file.read()
    if file_path.endswith(".py"):
        return chunk_python(code, file_path)
    elif file_path.endswith(".md"):
        return chunk_markdown(file_path, code)
    elif file_path.endswith(".txt"):
        return chunk_txt(file_path, code)


