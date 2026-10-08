from pathlib import Path
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter, Language
from chunker import Chunk
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
        # this part for the py file
        tree = ast.parse(code)
        lines = code.splitlines()
        if (len(code) <= MAX_CHARS):
            return [code]
        chunk = []
        for node in tree.body:
            chunk.extend(chunk_py_node(node, lines))
        return chunk
    elif file_path.endswith(".md"):
        #this part for the markdown file

        return chunk_markdown(code)
    elif file_path.endswith(".txt"):
        # txt file
        return chunk_txt(code)


# def chunk_py_node(node, lines , path):

#     start = node.lineno - 1
#     end = node.end_lineno
#     start_col = node.col_offset
#     end_col = node.end_col_offset
#     test = Chunk()

#     code = "\n".join(lines[start:end])
#     if len(code) <= MAX_CHARS:
#         return [code]
#     chunks = []
#     if not getattr(node, "body", None):
#         return split_long(code, MAX_CHARS)
#     index = 1
#     for child in node.body:
#         child_chunks = chunk_py_node(child, lines)
#         chunks.extend(child_chunks)
#         test(
#             id = index,
#             text = chunks,
#             first_char_index = start + start_col,
#             last_char_index = end + end_col
#             text_path = path,
#         )
#         print(f"{test.id}\n{test.text}\n{test.first_char_index}\n{test.last_char_index}\n{test.text_path}")
#     return chunks
# chunk_py_node()


def chunk_markdown() -> list[str]:

    with open("/Users/ameen/Desktop/RAG-douae/vllm_tester/README.md", "r") as file:
        text = file.read()
    chunk = Chunk()

    md_splitter = RecursiveCharacterTextSplitter.from_language(
        Language.MARKDOWN, chunk_size=MAX_CHARS, chunk_overlap=200
    )
    test = md_splitter.split_text(text)
    next_id = 1
    for i in range(len(test)):
        chunk(
            id = next_id,
            text = i,
            first_char_index = ...,
            last_char_index = ...,
            text_path = "/Users/ameen/Desktop/RAG-douae/vllm_tester/README.md"
        )
        next_id += 1
    print(len(test))

# chunk_markdown()
    


def chunk_txt(text) -> list[str]:

    with open("/Users/ameen/Desktop/RAG-douae/vllm_tester/text.txt", "r") as file:
        text = file.read()
    txt_splitter = RecursiveCharacterTextSplitter(
        chunk_size=MAX_CHARS, chunk_overlap=200
    )
    chunk = txt_splitter.split_text(text)
    return chunk
