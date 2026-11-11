from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from src.minimalsource import  BigChunk
from constants import DEFAULT_MAX_CHUNK_SIZE

def chunk_txt(path_file, text, max_chunk_size: int = DEFAULT_MAX_CHUNK_SIZE) -> list :

    chunks = []

    txt_splitter = RecursiveCharacterTextSplitter(
        chunk_size=max_chunk_size,
        chunk_overlap=min(200, max_chunk_size - 1),
        add_start_index=True,
    )
    docs = txt_splitter.create_documents([text])

    for i, info in enumerate(docs):

        start_index = info.metadata["start_index"]
        end_index = start_index + len(info.page_content)

        first_line = text.count('\n', 0, start_index) + 1
        last_line  = text.count('\n', 0, end_index - 1) + 1

        chunks.append(BigChunk(
            id = i,
            text = info.page_content,
            file_path=path_file,
            first_line= first_line,
            last_line=last_line,
            first_character_index=start_index,
            last_character_index=end_index,
        ))

    return chunks
