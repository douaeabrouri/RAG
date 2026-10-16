from pydantic import BaseModel
from pathlib import Path

ALLOWED_FILES = [".py", ".md", ".txt"]
MAX_CHARS = 2000
BASE_DIR = Path(__file__).resolve().parent
PATH = BASE_DIR.parent / "vllm_tester"

class MinimalSource(BaseModel) :
    id    : int
    text   : str
    file_path: Path
    first_line : int
    last_line  : int 
    first_char_index: int
    last_char_index: int


def get_files_path(root: str) -> list[Path]:
    files_paths: list[Path] = []

    for file in PATH.rglob("*"):
        if not file.is_file():
            continue
        if file.suffix not in ALLOWED_FILES:
            continue
        files_paths.append(file)
    return files_paths
