from constants import PATH1, ALLOWED_FILES
from pathlib import Path


ALL_FILES_PATH: list[str] = []


def get_files_path(root: str) -> list[Path]:
    files_paths: list[Path] = []

    for file in PATH1.rglob("*"):
        if not file.is_file():
            continue
        if file.suffix not in ALLOWED_FILES:
            continue
        files_paths.append(file)
    return files_paths

ALL_FILES_PATH = get_files_path(PATH1)