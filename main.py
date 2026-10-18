from chunking.chunker import  ALL_FILES_PATH
from indexing.bm25_ranking import search, build_index
from pydantic import BaseModel, Field
from pathlib import Path
from typing import List
import uuid
import json
from ollama import client
from constants import MODEL_NAME
import re

class MinimalSource(BaseModel) :
    id    : int
    text   : str
    file_path: Path
    first_line : int
    last_line  : int 
    first_char_index: int
    last_char_index: int

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
t = build_index(ALL_FILES_PATH)

for item in questions["rag_questions"]:
    source = []
    question = item["question"]
    sources = search(question, t, 5)
    if not sources:
        raise "I don't Know!"
    
    context = "\n\n---\n\n".join(s.text for s in sources)

    prompt = (
        "Answer in 1 to 3 sentences using only the context below. "
        "If the answer is not in the context, say you don't know.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question} /no_think"
    )
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    answer = response.choices[0].message.content or ""
    answer = re.sub(r"<think>.*?</think>", "", answer, flags=re.DOTALL).strip()
    print(answer)

    result.append(AnsweredQuestion(
        question_id = item["question_id"],
        question = question,
        sources = sources,
        answer = "",
    ))
