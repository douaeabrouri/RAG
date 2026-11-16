import ast
from pathlib import Path
from chunking.txt_chunker import chunk_txt
from constants import DEFAULT_MAX_CHUNK_SIZE
from src.minimalsource import BigChunk


def split_long(text: str, limit: int) -> list[str]:
    """Split text into contiguous pieces no longer than the specified limit.

    Args:
        text: Text to split without changing its characters.
        limit: Maximum number of characters in each returned piece.

    Returns:
        Text pieces whose lengths do not exceed ``limit``.
    """
    if limit <= 0:
        raise ValueError("limit must be positive")
    return [text[start:start + limit] for start in range(0, len(text), limit)]


def chunk_py_node(
    node: ast.AST,
    lines: list[str],
    source: str,
    pieces: list[tuple[str, int, int, int, int]],
    offsets: list[int],
    max_chunk_size: int,
) -> None:
    """Convert an AST node into one or more location-aware text pieces.

    Args:
        node: Python abstract-syntax-tree node to process.
        lines: Source code split into lines.
        pieces: Mutable list receiving text and source-location tuples.
        offsets: Character offsets for the start of each source line.
        max_chunk_size: Maximum number of characters allowed per piece.

    Returns:
        None. Results are appended to ``pieces``.
    """

    start = node.lineno
    end = node.end_lineno
    first_char_index = offsets[start - 1]
    last_char_index = offsets[end - 1] + len(
        lines[end - 1].rstrip("\r\n")
    )
    code = source[first_char_index:last_char_index]
    children = getattr(node, "body", None)

    if len(code) <= max_chunk_size:
        pieces.append((code, start, end, first_char_index, last_char_index))

    elif isinstance(children, list) and children:
        for child in children:
            chunk_py_node(
                child, lines, source, pieces, offsets, max_chunk_size
            )
        return

    else:
        pos = first_char_index
        for part in split_long(code, max_chunk_size):
            pieces.append((part, start, end, pos, pos + len(part)))
            pos += len(part)


def pack(
    pieces: list[tuple[str, int, int, int, int]],
    path: str | Path,
    max_chunk_size: int,
) -> list[BigChunk]:
    """Pack adjacent source pieces into chunks within the size limit.

    Args:
        pieces: Source text and location tuples to combine.
        path: Path of the source file represented by the pieces.
        max_chunk_size: Maximum number of characters per resulting chunk.

    Returns:
        ``BigChunk`` instances containing packed text and source locations.
    """

    chunks: list[BigChunk] = []
    cur: list[str | int | None] | None = None

    def flush() -> None:
        """Append the current packed piece as a ``BigChunk``."""
        assert cur is not None
        chunks.append(
            BigChunk(
                id=len(chunks),
                text=str(cur[0]),
                file_path=path,
                first_line=int(cur[1]),
                last_line=int(cur[2]),
                first_character_index=int(cur[3]),
                last_character_index=int(cur[4]),
            )
        )

    for text, fl, ll, fc, lc in pieces:
        exceeds_text_limit = (
            cur is not None
            and len(str(cur[0])) + 2 + len(text) > max_chunk_size
        )
        exceeds_source_limit = (
            cur is not None
            and lc - int(cur[3]) > max_chunk_size
        )
        if cur and (exceeds_text_limit or exceeds_source_limit):
            flush()
            cur = None
        if cur:
            cur[0] = str(cur[0]) + "\n\n" + text
            cur[2] = ll
            cur[4] = lc
        else:
            cur = [text, fl, ll, fc, lc]

    if cur:
        flush()
    return chunks


def chunk_python(
    code: str,
    file_path: str | Path,
    max_chunk_size: int = DEFAULT_MAX_CHUNK_SIZE,
) -> list[BigChunk]:
    """Chunk Python source by AST structure, falling back to text splitting.

    Args:
        code: Complete Python source text.
        file_path: Path of the source file, stored in chunk metadata.
        max_chunk_size: Maximum number of characters per chunk.

    Returns:
        ``BigChunk`` instances containing source text and location metadata.
    """
    if max_chunk_size <= 0:
        raise ValueError("max_chunk_size must be positive")

    try:
        tree = ast.parse(code, filename=str(file_path))
    except SyntaxError:
        return chunk_txt(file_path, code, max_chunk_size)
    lines = code.splitlines(keepends=True)

    offsets = [0]
    for line in code.splitlines(keepends=True):
        offsets.append(offsets[-1] + len(line))

    chunks = []
    for node in tree.body:
        chunk_py_node(
            node, lines, code, chunks, offsets, max_chunk_size
        )
    chunk = pack(chunks, file_path, max_chunk_size)
    too_long = [
        c for c in chunk
        if c.last_character_index - c.first_character_index > max_chunk_size
    ]
    if too_long:
        raise ValueError(
            f"Chunk source range exceeds the {max_chunk_size}-character limit"
        )

    return chunk
