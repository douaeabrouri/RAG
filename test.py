from main import split_long
from chunker import Chunk
import ast
def chunk_py_node(node, lines, path, chunks):

    start = node.lineno - 1
    end = node.end_lineno
    # start_col = node.col_offset
    # end_col = node.end_col_offset
    code = "\n".join(lines[start:end])
    children = getattr(node, "body", None)

    if len(code) <= MAX_CHARS:
        piece = [code]

    elif isinstance(children, list) and children:
        for child in children:
            chunk_py_node(child, lines, path, chunks)
        return

    else:
        pieces = split_long(code, MAX_CHARS)

    for piece in pieces:
        chunks.append(Chunk(
            id=len(chunks),
            text=piece,
            text_path=path,
            first_line=start,
            last_line=end,
        ))

if __name__ == "__main__":

    MAX_CHARS = 2000
    file_path = "/home/doabrour/Desktop/RAG/vllm_tester/file.py"

    with open(file_path, "r") as file:
        code = file.read()
    tree = ast.parse(code)
    lines = code.splitlines()

    chunks = []
    for node in tree.body:
        chunk_py_node(node, lines, file_path, chunks)

    for c in chunks:
        print(f"Chunk id: {c.id}, first line: {c.first_line}")
       