from pathlib import Path
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter, Language
from chunker import MinimalSource, MAX_CHARS, ALLOWED_FILES
import ast

PATH = Path("/Users/ameen/Desktop/RAG-douae/vllm_tester")

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

def chunk_py_node(node, lines, pieces, offsets):

    start = node.lineno
    end = node.end_lineno
    first_char_index = offsets[start - 1]
    last_char_index = offsets[end - 1] + len(lines[end - 1])
    code = "\n".join(lines[start - 1:end])
    children = getattr(node, "body", None)

    # pieces = []
    if len(code) <= MAX_CHARS:
        pieces.append((code, start, end, first_char_index, last_char_index))

    elif isinstance(children, list) and children:
        for child in children:
            chunk_py_node(child, lines ,pieces, offsets)
        return

    else:
        pos = first_char_index
        for part in split_long(code, MAX_CHARS):
            pieces.append((part, start, end, pos, pos + len(part)))
            pos += len(part)
    
def pack(pieces, path):

    chunks: list[MinimalSource] = []
    cur = None   # [text, first_line, last_line, first_char, last_char]

    def flush():
        chunks.append(MinimalSource(
            id=len(chunks), text=cur[0], file_path=path,
            first_line=cur[1], last_line=cur[2],
            first_char_index=cur[3], last_char_index=cur[4],
        ))

    for text, fl, ll, fc, lc in pieces:
        if cur and len(cur[0]) + 2 + len(text) > MAX_CHARS:
            flush()
            cur = None
        if cur:
            cur[0] += "\n\n" + text
            cur[2] = ll          
            cur[4] = lc
        else:
            cur = [text, fl, ll, fc, lc]

    if cur:
        flush()
    return chunks

def chunk_python(code, file_path):

    tree = ast.parse(code)
    lines = code.splitlines()

    offsets = [0]
    for line in code.splitlines(keepends=True):
        offsets.append(offsets[-1] + len(line))

    chunks = []
    for node in tree.body:
        chunk_py_node(node, lines, chunks, offsets)
    chunk = pack(chunks, file_path)

    return chunk


def chunk_markdown(path_file, text) -> list:

    chunks = []
    md_splitter = RecursiveCharacterTextSplitter.from_language(
        Language.MARKDOWN, chunk_size=MAX_CHARS, chunk_overlap=200, add_start_index=True,
    )

    docs = md_splitter.create_documents([text])
    for i, info in enumerate(docs):
        start_index = info.metadata["start_index"]
        end_index = start_index + len(info.page_content)

        first_line = text.count('\n', 0, start_index) + 1
        last_line  = text.count('\n', 0, end_index - 1) + 1

        chunks.append(MinimalSource(
            id = i,
            text = info.page_content,
            file_path=path_file,
            first_line= first_line,
            last_line=last_line,
            first_char_index=start_index,
            last_char_index=end_index,
        ))
    return chunks


def chunk_txt(path_file, text) -> list[str]:

    chunks = []

    txt_splitter = RecursiveCharacterTextSplitter(
        chunk_size=MAX_CHARS, chunk_overlap=200
    )
    docs = txt_splitter.create_documents(text)

    for i, info in enumerate(docs):
        start_index = info.metadata["start_index"]
        end_index = start_index + len(info.page_content)

        first_line = text.count('\n', 0, start_index) + 1
        last_line  = text.count('\n', 0, end_index - 1) + 1

        chunks.append(MinimalSource(
            id = i,
            text = info.page_content,
            file_path=path_file,
            first_line= first_line,
            last_line=last_line,
            first_char_index=start_index,
            last_char_index=end_index,
        ))

    return chunks
