from pydantic import BaseModel
from pathlib import Path


class Source(BaseModel):
    file_path: Path
    first_char_index: int
    last_char_index: int

class MinimalSource(BaseModel) :
    id    : int
    text   : str
    file_path: Path
    first_line : int
    last_line  : int 
    first_char_index: int
    last_char_index: int