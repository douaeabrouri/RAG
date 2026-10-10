from pydantic import BaseModel

ALLOWED_FILES = [".py", ".md", ".txt"]
MAX_CHARS = 2000
class MinimalSource(BaseModel) :
    id    : int
    text   : str
    file_path: str
    first_line : int
    last_line  : int 
    first_char_index: int
    last_char_index: int
