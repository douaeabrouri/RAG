from main import split_long
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from chunker import MinimalSource, MAX_CHARS
import ast

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
            file_path=file_path,
            first_line= first_line,
            last_line=last_line,
            first_char_index=start_index,
            last_char_index=end_index,
        ))
    return chunks


if __name__ == "__main__":

    file_path = "/Users/ameen/Desktop/RAG/vllm_tester/README.md"

    with open(file_path, "r") as file:
        text = file.read()

    test = chunk_markdown(file_path, text)
    for info in test:
        print(f"{info.first_line},{info.last_line}")
    

