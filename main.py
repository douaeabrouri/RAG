from pathlib import Path
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
import ast

PATH = Path("/Users/ameen/Desktop/RAG-douae/vllm_tester")
MAX_CHARS = 2000
allowed_files = [".py", ".md", ".txt"]

def split_long(text: str, limit: int) -> str:

    void : str = ""
    part : list[str] = []

    for line in text.splitlines():
        while(len(line) > limit):
            if void:
                part.append(void)
                void = ""
            part.append(line[:limit])
            line = line[limit:]
        if void and len(void) + len(line) > limit:
            part.append(void)
            void = ""
        void += line
    if void:
        part.append(void)
    return part


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


def chunking_file(file_path: Path):
    with open("/Users/ameen/Desktop/RAG-douae/vllm_tester/file.py", "r") as file:
        code = file.read()
    if file_path.endswith(".py"):
        tree = ast.parse(code)
        lines = code.splitlines()
        if (len(code) <= MAX_CHARS):
            return [code]
        
        chunk = []
        for node in tree.body:
            chunk.extend(chunk_py_node(node, lines))
        return chunk
    else:
        ...


def chunk_py_node(node, lines):

    start = node.lineno - 1
    end = node.end_lineno

    code = "\n".join(lines[start:end])
    if len(code) <= MAX_CHARS:
        return [code]
    chunks = []
    if not getattr(node, "body", None):
        return split_long(code, MAX_CHARS)
    for child in node.body:
        child_chunks = chunk_py_node(child, lines)
        chunks.extend(child_chunks)
    return chunks

def chunk_markdown():
    with open("/Users/ameen/Desktop/RAG-douae/vllm_tester/README.md", "r") as file:
        code = file.read()
    headers_t = [('#', "headear 1"), ('##', "headear 2"), ('###', "headear 3")]
    markdown_file = MarkdownHeaderTextSplitter(headers_t, False)
    md_header = markdown_file.split_text(code)
    size_spliter = RecursiveCharacterTextSplitter(
        chunk_size=MAX_CHARS,
        chunk_overlap=200,
    )
    docs = size_spliter.split_documents(md_header)
    print([d.page_content for d in docs])
    # print(docs)
chunk_markdown()


def chunk_txt_node():
    ...
