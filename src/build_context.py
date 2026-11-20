
def build_context(chunks):
    """Read source ranges and format them as labeled context blocks.

    Args:
        chunks: Mapping-like chunk records with file paths and character
            offsets.

    Returns:
        Context text containing each source path and its selected contents.
    """
    blocks = []

    for chunk in chunks:
        if isinstance(chunk, dict):
            file_path = chunk["file_path"]
            first_index = int(chunk["first_character_index"])
            last_index = int(chunk["last_character_index"])
        else:
            file_path = str(chunk.file_path)
            first_index = int(chunk.first_character_index)
            last_index = int(chunk.last_character_index)

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        chunk_text = content[first_index:last_index]

        blocks.append(
            f"[source: {file_path}]\n{chunk_text}"
        )

    return "\n---\n".join(blocks)
