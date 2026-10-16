from chunking.chunker import MinimalSource, ALL_FILES_PATH
from .bm25_ranking import search, build_index
from pydantic import BaseModel, Field
from pathlib import Path
from typing import List
import uuid
import json

class UnansweredQuestion(BaseModel):
    question_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    question: str
class AnsweredQuestion(UnansweredQuestion):
    sources: List[MinimalSource]
    answer: str


BASE_DIR = Path(__file__).resolve().parent
PATH = BASE_DIR.parent / "data/input"

with open(PATH / "dataset_code_public.json", "r") as file:
    questions = json.load(file)

result = []

for item in questions["rag_questions"]:
    for path, start, end in search(item["question"], build_index(ALL_FILES_PATH), 5):
        result.append(UnansweredQuestion(
            question_id = item["question_id"],
            question = item["question"]
        ))
        result.append(AnsweredQuestion(
            sources = [
                file_path=path,
                first_character_index = start,
                last_character_index = end
            ],
            answer=
        ))




