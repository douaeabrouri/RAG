
def build_context(chunks):
    """Read source ranges and format them as labeled context blocks.

    Args:
        chunks: Mapping-like chunk records with file paths and character
            offsets.

    Returns:
        Context text containing each source path and its selected contents.
    """
    blocks = []

    for c in chunks:
        file_path = c["file_path"]
        first_index = int(c["first_character_index"])
        last_index = int(c["last_character_index"])

        with open(file_path, "r") as file:
            content = file.read()

        chunk_text = content[first_index:last_index]

        blocks.append(
            f"[source: {file_path}]\n{chunk_text}"
        )

    return "\n---\n".join(blocks)
