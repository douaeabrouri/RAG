from src.constants import ALLOWED_FILES
from pathlib import Path


def get_files_path(root: str) -> list[Path]:
    """Find supported files recursively under a directory.

    Args:
        root: Directory to search for supported source and documentation files.

    Returns:
        Paths to files whose suffix is listed in ``ALLOWED_FILES``.
    """
    files_paths: list[Path] = []

    for file in root.rglob("*"):
        if not file.is_file():
            continue
        if file.suffix not in ALLOWED_FILES:
            continue
        files_paths.append(file)
    return files_paths
