from pydantic import BaseModel
from pathlib import Path
from typing import List

class BigChunk(BaseModel):
    id    : int
    text   : str
    file_path: Path
    first_line : int
    last_line  : int 
    first_char_index: int
    last_char_index: int

class MinimalSource(BaseModel):
    file_path: str
    first_char_index: int
    last_char_index: int

class MinimalSearchResults(BaseModel):
    question_id: str
    question: str
    retrieved_sources: List[MinimalSource]

class MinimalAnswer(MinimalSearchResults):
    answer: str