from chunking.chunker import get_files_path, PATH
from chunking.models import chunking_files

ALL_FILES_PATH: list[str] = []
ALL_FILES_PATH = get_files_path(PATH)


result: list = []
for path in ALL_FILES_PATH:
    print(path)
    result = chunking_files(path)


# TODO: Ranks documents based on query-term matches, rarity, frequency, and document length.




