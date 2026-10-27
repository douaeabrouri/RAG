from chunking.chunker import  ALL_FILES_PATH
from indexing.bm25_ranking import search, build_index
from pathlib import Path
import json
from constants import MODEL_NAME, CLIENT, K, EXIT_FILES, BASE_DIR, FILE1
from build_context import build_context
from src.minimalsource import MinimalSource, MinimalAnswer, MinimalSearchResults
from managing_answers.save import save_answered, save_unanswered
import re
import sys


PATH = BASE_DIR / "data" / "datasets_public" / "public" / "UnansweredQuestions"
FILE1 = PATH / "dataset_code_public.json"

OUT_PATH = BASE_DIR / "data" / "output" / "search_results_and_answer" / "AnsweredQuestions"
output_file = OUT_PATH / "dataset_code_public.json"
output_file.parent.mkdir(parents=True, exist_ok=True)
OUT_PATH1 = BASE_DIR / "data" / "output" / "search_results" / "AnsweredQuestions"
output_file1 = OUT_PATH / "dataset_code_public.json"
output_file1.parent.mkdir(parents=True, exist_ok=True)


def to_source(top_chunks) -> list[MinimalAnswer]:
    return [
        MinimalSource(
            file_path = str(c.file_path),
            first_char_index = str(c.first_char_index),
            last_char_index = str(c.last_char_index),
        )
        for c in top_chunks
    ]

def make_prompt(question, top_chunks) -> str:
    context = build_context(top_chunks)
    return (
        "Answer in 1 to 3 sentences using only the context below. "
        "If the answer is not in the context, say you don't know.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question} /no_think"
    )


def ask_llm(question, chunks) -> str:
    response = CLIENT.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": make_prompt(question, chunks)}],
        options={"temperature": 0},
    )
    answer = response.message.content or ""
    return re.sub(r"<think>.*?</think>", "", answer, flags=re.DOTALL).strip()



if  __name__ == "__main__" :

    with open(FILE1, "r") as file:
        questions = json.load(file) 


    t = build_index(ALL_FILES_PATH)
    searched = []
    chunks_by_id = {}
    for item in questions["rag_questions"]:
        top_chunks = search(item["question"], t, K)
        chunks_by_id[item["question_id"]] = top_chunks
        searched.append(MinimalSearchResults(
            question_id=item["question_id"],
            question=item["question"],
            retrieved_sources = to_source(top_chunks),
        ))
        if item["question"].lower() in EXIT_FILES :
            sys.exit()

        save_unanswered(searched, K, output_file1)

    answered = []
    for item in questions["rag_questions"]:
        top_chunks = chunks_by_id[item["question_id"]]
        if top_chunks:
            answer = ask_llm(make_prompt(item["question"], top_chunks))
        else:
            answer =  "I don't Know!"
            retrieved_sources = []

        answered.append(MinimalAnswer(
            question_id=item["question_id"],
            question=item["question"],
            retrieved_sources=to_source(top_chunks),
            answer=answer,
        ))
        save_answered(answered, K, output_file)




        
