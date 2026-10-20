from chunking.chunker import  ALL_FILES_PATH
from indexing.bm25_ranking import search, build_index
from pathlib import Path
import json
from constants import MODEL_NAME
import re
from src.answerdquestion import AnsweredQuestion
from ollama import Client


BASE_DIR = Path(__file__).resolve().parent
PATH = BASE_DIR / "data" / "input"
f = PATH / "dataset_code_public.json"

with open(f, "r") as file:
    questions = json.load(file)
print("folder:", PATH, "| exists:", PATH.exists())
print("everything inside:", list(PATH.rglob("*"))[:10])

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
    response = Client.chat.completions.create(
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
