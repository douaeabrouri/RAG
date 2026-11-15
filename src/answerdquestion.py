from .minimalsource import MinimalSource
from typing import List
import uuid
from pydantic import BaseModel, Field


class UnansweredQuestion(BaseModel):
    """Dataset question record that does not include an answer or sources.

    Attributes:
        question_id: Unique identifier generated when one is not provided.
        question: Natural-language question text.
    """
    question_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    question: str


class AnsweredQuestion(UnansweredQuestion):
    """Dataset question annotated with its reference sources and answer.

    Attributes:
        sources: Ground-truth source ranges relevant to the question.
        answer: Reference answer text.
    """
    sources: List[MinimalSource]
    answer: str


class RagDataset(BaseModel):
    """Collection of answered and unanswered RAG evaluation questions.

    Attributes:
        rag_questions: Dataset question records.
    """
    rag_questions: List[AnsweredQuestion | UnansweredQuestion]
