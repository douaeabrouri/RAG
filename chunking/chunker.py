from constants import  ALLOWED_FILES
from pathlib import Path


def get_files_path(root: str) -> list[Path]:
    files_paths: list[Path] = []

    for file in root.rglob("*"):
        if not file.is_file():
            continue
        if file.suffix not in ALLOWED_FILES:
            continue
        files_paths.append(file)
    return files_paths
