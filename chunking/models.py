from chunking.markdown_chunker import chunk_markdown
from chunking.python_chunker import chunk_python
from chunking.txt_chunker import chunk_txt
from pathlib import Path


def chunking_files(file_path: Path):
    
    with open("/Users/ameen/Desktop/RAG/vllm_tester/file.py", "r") as file:
        code = file.read()
    if file_path.endswith(".py"):
        return chunk_python(code, file_path)
    elif file_path.endswith(".md"):
        return chunk_markdown(file_path, code)
    elif file_path.endswith(".txt"):
        return chunk_txt(file_path, code)