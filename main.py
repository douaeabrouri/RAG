from chunking.chunker import  ALL_FILES_PATH
from indexing.bm25_ranking import search, build_index
from pathlib import Path
import json
from constants import MODEL_NAME, Client, K
from src.answerdquestion import AnsweredQuestion
from build_context import build_context
from src.minimalsource import MinimalSource, MinimalAnswer, MinimalSearchResults
from src.search_result import StudentSearchResultsAndAnswer, StudentSearchResults
import re
import sys


BASE_DIR = Path(__file__).resolve().parent
PATH = BASE_DIR / "data" / "input"
f = PATH / "dataset_code_public.json"

exit_list = ["bye", "exit", "quit", "q", "close"]

OUT_PATH = BASE_DIR / "data" / "output"
output_file = OUT_PATH / "dataset_code_public.json"
output_file.parent.mkdir(parents=True, exist_ok=True)

def save(result, k, path):
    output = StudentSearchResultsAndAnswer(search_results=result, k=k)
    with open(path, "w") as file:
        json.dump(output.model_dump(mode="json"), file, indent=3, ensure_ascii=False)

def save2(result, K, path):
    output = StudentSearchResults(search_results=result, k=K)
    with open(path, "w") as file:
            json.dump(output.model_dump(mode="json"), file, indent=3, ensure_ascii=False)

if __name__ == "__main__" :

    with open(f, "r") as file:
        questions = json.load(file) 

    result = []
    result1 = []
    t = build_index(ALL_FILES_PATH)

    for item in questions["rag_questions"]:
        retrieved_sources = []
        question = item["question"]
        top_chunks = search(question, t, K)
        if not top_chunks:
            answer =  "I don't Know!"
            retrieved_sources = []
        if question.lower() in exit_list :
            sys.exit()

        else:
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
                options={"temperature": 0},
            )
            answer = response.message.content or ""
            answer = re.sub(r"<think>.*?</think>", "", answer, flags=re.DOTALL).strip()

            retrieved_sources = [
                MinimalSource(
                    file_path = str(c.file_path),
                    first_char_index = str(c.first_char_index),
                    last_char_index = str(c.last_char_index),
                )
                for c in top_chunks
            ]

            result.append(MinimalAnswer(
                question_id = item["question_id"],
                question = question,
                retrieved_sources = retrieved_sources,
                answer = answer,
            ))

            result1.append(MinimalSearchResults(
                question_id = item["question_id"],
                question = question,
                retrieved_sources = retrieved_sources,                
            ))

            save(result, K, output_file)
            save2(result1, K, ...)
        
