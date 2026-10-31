
def build_context(chunks):
    blocks = []

    for c in chunks:
        file_path = c["file_path"]
        first_index = int(c["first_charactere_index"])
        last_index = int(c["last_charactere_index"])

        with open(file_path, "r") as file:
            content = file.read()

        chunk_text = content[first_index:last_index]

        blocks.append(
            f"[source: {file_path}]\n{chunk_text}"
        )

    return "\n---\n".join(blocks)