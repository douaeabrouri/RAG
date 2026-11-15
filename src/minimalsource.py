from pydantic import BaseModel
from pathlib import Path
from typing import List

class BigChunk(BaseModel):
    """Text chunk plus its source file and line/character boundaries.

    Attributes:
        id: Chunk identifier within its source file.
        text: Text content stored in the chunk.
        file_path: Path of the source file.
        first_line: One-based first source line represented by the chunk.
        last_line: One-based last source line represented by the chunk.
        first_character_index: Inclusive starting character offset.
        last_character_index: Exclusive ending character offset.
    """
    id    : int
    text   : str
    file_path: Path
    first_line : int
    last_line  : int 
    first_character_index: int
    last_character_index: int

class MinimalSource(BaseModel):
    """Compact reference to a source range in a file.

    Attributes:
        file_path: Path of the referenced file.
        first_character_index: Inclusive starting character offset.
        last_character_index: Exclusive ending character offset.
    """
    file_path: str
    first_character_index: int
    last_character_index: int

class MinimalSearchResults(BaseModel):
    """Search results associated with one dataset question.

    Attributes:
        question_id: Unique identifier for the question.
        question: Natural-language question text.
        retrieved_sources: Source ranges returned by retrieval.
    """
    question_id: str
    question: str
    retrieved_sources: List[MinimalSource]

class MinimalAnswer(MinimalSearchResults):
    """Search-result record augmented with a generated answer.

    Attributes:
        answer: Answer generated from the retrieved source context.
    """
    answer: str