

def build_context(chunks):
    blocks = []
    for c in chunks:
        blocks.append(
            f"[source: {c.file_path} | chars {c.first_char_index}-{c.last_char_index}]\n{c.text}"
        )
    return "\n---\n".join(blocks)
     