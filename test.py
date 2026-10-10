from main import split_long
from chunker import Chunk
import ast

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

    chunks: list[Chunk] = []
    cur = None   # [text, first_line, last_line, first_char, last_char]

    def flush():
        chunks.append(Chunk(
            id=len(chunks), text=cur[0], text_path=path,
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


if __name__ == "__main__":

    MAX_CHARS = 2000
    file_path = "/Users/ameen/Desktop/RAG/vllm_tester/file.py"

    with open(file_path, "r") as file:
        code = file.read()
    print(len(code))
    tree = ast.parse(code)
    lines = code.splitlines()

    offsets = [0]
    for line in code.splitlines(keepends=True):
        offsets.append(offsets[-1] + len(line))

    chunks = []
    for node in tree.body:
        chunk_py_node(node, lines, chunks, offsets)

    chunk = pack(chunks, file_path)

    for c in chunk:
        print("haaaaaaa wahd")
        print(f"chunk id: {c.id}, first line: {c.first_line}, last line: {c.last_line}, first index {c.first_char_index}, last index {c.last_char_index}, text: {c.text}")
