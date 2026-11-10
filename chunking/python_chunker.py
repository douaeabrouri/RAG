import ast
from src.minimalsource import  BigChunk
from chunking.txt_chunker import chunk_txt
from constants import DEFAULT_MAX_CHUNK_SIZE

def split_long(text: str, limit: int) -> list[str]:

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

def chunk_py_node(node, lines, pieces, offsets, max_chunk_size):

    start = node.lineno
    end = node.end_lineno
    first_char_index = offsets[start - 1]
    last_char_index = offsets[end - 1] + len(lines[end - 1])
    code = "\n".join(lines[start - 1:end])
    children = getattr(node, "body", None)

    # pieces = []
    if len(code) <= max_chunk_size:
        pieces.append((code, start, end, first_char_index, last_char_index))

    elif isinstance(children, list) and children:
        for child in children:
            chunk_py_node(child, lines, pieces, offsets, max_chunk_size)
        return

    else:
        pos = first_char_index
        for part in split_long(code, max_chunk_size):
            pieces.append((part, start, end, pos, pos + len(part)))
            pos += len(part)
    
def pack(pieces, path, max_chunk_size):

    chunks: list[BigChunk] = []
    cur = None   # [text, first_line, last_line, first_char, last_char]

    def flush():
        chunks.append(BigChunk(
            id=len(chunks), text=cur[0], file_path=path,
            first_line=cur[1], last_line=cur[2],
            first_character_index=cur[3], last_character_index=cur[4],
        ))

    for text, fl, ll, fc, lc in pieces:
        if cur and len(cur[0]) + 2 + len(text) > max_chunk_size:
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

def chunk_python(code, file_path, max_chunk_size: int = DEFAULT_MAX_CHUNK_SIZE):
    try:
        tree = ast.parse(code, filename=str(file_path))
    except SyntaxError:
        return chunk_txt(file_path, code, max_chunk_size)
    lines = code.splitlines()

    offsets = [0]
    for line in code.splitlines(keepends=True):
        offsets.append(offsets[-1] + len(line))

    chunks = []
    for node in tree.body:
        chunk_py_node(node, lines, chunks, offsets, max_chunk_size)
    chunk = pack(chunks, file_path, max_chunk_size)

    return chunk
