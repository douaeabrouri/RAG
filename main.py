from chunking.chunker import  ALL_FILES_PATH
from indexing.bm25_ranking import search, build_index
from pathlib import Path
import json
from constants import MODEL_NAME, Client
import re
from src.answerdquestion import AnsweredQuestion
from src.minimalsource import Source
import sys
from build_context import build_context


BASE_DIR = Path(__file__).resolve().parent
PATH = BASE_DIR / "data" / "input"
f = PATH / "dataset_code_public.json"

exit_list = ["bye", "exit", "quit", "q", "close"]

OUT_PATH = BASE_DIR / "data" / "output"
output_file = OUT_PATH / "dataset_code_public.json"
output_file.parent.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__" :

    with open(f, "r") as file:
        questions = json.load(file)

    result = []
    t = build_index(ALL_FILES_PATH)

    for item in questions["rag_questions"]:
        question = item["question"]
        top_chunks = search(question, t, 5)

        if not top_chunks:
            answer =  "I don't Know!"
            source = []
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
        
            sources = [
                Source(
                    file_path = str(c.file_path),
                    first_char_index = str(c.first_char_index),
                    last_char_index = str(c.last_char_index),
                )
                for c in top_chunks
            ]
            result.append(AnsweredQuestion(
                question_id = item["question_id"],
                question = question,
                sources = sources,
                answer = answer,
            ))    

    with open(output_file, "w") as file:
        json.dump([obj.model_dump(mode="json") for obj in result], file, indent=3, ensure_ascii=False)
        
