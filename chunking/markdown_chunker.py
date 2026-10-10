from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from chunker import MAX_CHARS, MinimalSource


def chunk_markdown(path_file, text) -> list:

    chunks = []
    md_splitter = RecursiveCharacterTextSplitter.from_language(
        Language.MARKDOWN, chunk_size=MAX_CHARS, chunk_overlap=200, add_start_index=True,
    )

    docs = md_splitter.create_documents([text])
    for i, info in enumerate(docs):
        start_index = info.metadata["start_index"]
        end_index = start_index + len(info.page_content)

        first_line = text.count('\n', 0, start_index) + 1
        last_line  = text.count('\n', 0, end_index - 1) + 1

        chunks.append(MinimalSource(
            id = i,
            text = info.page_content,
            file_path=path_file,
            first_line= first_line,
            last_line=last_line,
            first_char_index=start_index,
            last_char_index=end_index,
        ))
    return chunks
