from chunking.chunker import  ALL_FILES_PATH
from indexing.bm25_ranking import search, build_index
from pathlib import Path
import json
from constants import MODEL_NAME, Client
import re
from src.answerdquestion import AnsweredQuestion
import sys
from build_context import build_context


BASE_DIR = Path(__file__).resolve().parent
PATH = BASE_DIR / "data" / "input"
f = PATH / "dataset_code_public.json"

exit_list = ["bye", "exit", "quit", "q", "close"]


if __name__ == "__main__" :

    with open(f, "r") as file:
        questions = json.load(file)

    result = []
    t = build_index(ALL_FILES_PATH)

    for item in questions["rag_questions"]:
        question = item["question"]
        top_chunks = search(question, t, 5)

        if not question == "" :
            continue
        if question.lower() in exit_list :
            sys.exit()

        if not top_chunks:
            raise "I don't Know!"
        context = build_context(top_chunks)
        prompt = (
            "Answer in 1 to 3 sentences using only the context below. "
            "If the answer is not in the context, say you don't know.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {question} /no_think"
        )

        response = Client.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0, "stream" : True},
        )
        answer = response.message.content or ""
        answer = re.sub(r"<think>.*?</think>", "", answer, flags=re.DOTALL).strip()
        source = [
            {"file_path": c.file_path,
            "first_char_index": c.first_char_index,
            "last_char_index": c.last_char_index}
            for c in top_chunks
        ]
        result.append(AnsweredQuestion(
            question_id = item["question_id"],
            question = question,
            sources = source,
            answer = "",
        ))
    
