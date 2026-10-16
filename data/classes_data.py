from typing import List
from pydantic import BaseModel
from chunking.chunker import MinimalSource
from dataclasses import Field
import uuid


class UnansweredQuestion(BaseModel):
    question_id: str = Field(default_factory=lambda:
    str(uuid.uuid4()))
    question: str


class AnsweredQuestion(UnansweredQuestion):
    sources: List[MinimalSource]
    answer: str

