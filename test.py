from main import split_long
from chunker import Chunk

MAX_CHARS = 2000

def chunk_py_node(node, lines , path):

    start = node.lineno - 1
    end = node.end_lineno
    start_col = node.col_offset
    end_col = node.end_col_offset
    test = Chunk()

    code = "\n".join(lines[start:end])
    if len(code) <= MAX_CHARS:
        return [code]
    chunks = []
    if not getattr(node, "body", None):
        return split_long(code, MAX_CHARS)
    index = 1
    for child in node.body:
        child_chunks = chunk_py_node(child, lines)
        chunks.extend(child_chunks)
        test(
            id = index,
            text = chunks,
            first_char_index = start + start_col,
            last_char_index = end + end_col
            text_path = path,
        )
        print(f"{test.id}\n{test.text}\n{test.first_char_index}\n{test.last_char_index}\n{test.text_path}")
    return chunks