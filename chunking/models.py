from chunking.markdown_chunker import chunk_markdown
from chunking.python_chunker import chunk_python
from chunking.txt_chunker import chunk_txt
from pathlib import Path
from constants import DEFAULT_MAX_CHUNK_SIZE


def chunking_files(
    file_path: Path,
    max_chunk_size: int = DEFAULT_MAX_CHUNK_SIZE
) -> list:
    """Read and chunk a supported file using its format-specific splitter.

    Args:
        file_path: Path to the file to read and split.
        max_chunk_size: Maximum number of characters per chunk.

    Returns:
        Chunks produced by the splitter for the file's format, or ``None``
        when the file suffix is unsupported.
    """

    with open(file_path, "r") as file:
        code = file.read()
    if file_path.suffix == ".py":
        return chunk_python(code, file_path, max_chunk_size)
    if file_path.suffix == ".md":
        return chunk_markdown(file_path, code, max_chunk_size)
    if file_path.suffix == ".txt":
        return chunk_txt(file_path, code, max_chunk_size)
    return []
