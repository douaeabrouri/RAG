from pathlib import Path
import os, ast
import linecache
import traceback

PATH = Path("/Users/ameen/Desktop/RAG-douae/vllm_tester")
MAX_CHARS = 2000
allowed_files = [".py", ".md", ".txt"]


# sterp 1 -> scan repo on the folder and t check if there inside allowed_files

def get_files_path(root: str) -> list[Path]:
    files_paths: list[Path] = []

    for file in PATH.rglob("*"):
        if not file.is_file():
            continue
        if file.suffix not in allowed_files:
            continue
        print(file)
        files_paths.append(file)
    return files_paths

# step 2 -> chunking

def chunk_file(file_path: Path):
    if file_path.endswith(".py"):
        ...
    else:
        ...

def chunk_node(node, lines):
    start = node.lineno - 1
    end = node.end_lineno

    code = "".join(lines[start:end])

    if len(code) <= MAX_CHARS:
        return [code]

    chunks = []
    for child in node.body:
        child_chunks = chunk_node(child, lines)
        chunks.extend(child_chunks)
    return chunks


def test():
    with open("/Users/ameen/Desktop/RAG-douae/vllm_tester/file.py", "r") as file:
        code = file.read()
        tree = ast.parse(code)
    chunk = []
    lines = code.splitlines()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Assign, ast.Import, ast.ImportFrom)):
            chunk.append(chunk_node(node, lines))
    print(chunk)

test()