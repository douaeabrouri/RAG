from chunking.markdown_chunker import chunk_markdown
from chunking.python_chunker import chunk_python
from chunking.txt_chunker import chunk_txt
from pathlib import Path


def chunking_files(file_path: Path):

    with open(file_path, "r") as file:
        code = file.read()
    if file_path.suffix == ".py":
        return chunk_python(code, file_path)
    elif file_path.suffix == ".md":
        return chunk_markdown(file_path, code)
    elif file_path.suffix == ".txt":
        return chunk_txt(file_path, code)