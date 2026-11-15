
from pydantic import BaseModel
from .minimalsource import MinimalSearchResults, MinimalAnswer
from typing import List


class StudentSearchResults(BaseModel):
    """Serialized retrieval output for a collection of questions.

    Attributes:
        search_results: Per-question retrieved source records.
        k: Number of results requested per question.
    """
    search_results: List[MinimalSearchResults]
    k: int


class StudentSearchResultsAndAnswer(BaseModel):
    """Serialized retrieval output with generated answers included.

    Attributes:
        search_results: Per-question retrieval and answer records.
        k: Number of results requested per question.
    """
    search_results: List[MinimalAnswer]
    k: int