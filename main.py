from chunking.chunker import  ALL_FILES_PATH
from indexing.bm25_ranking import search, build_index
from pathlib import Path
import json
from constants import MODEL_NAME, Client
import re
from src.answerdquestion import AnsweredQuestion
import ollama
from build_context import build_context


BASE_DIR = Path(__file__).resolve().parent
PATH = BASE_DIR / "data" / "input"
f = PATH / "dataset_code_public.json"


if __name__ == "__main__" :

    with open(f, "r") as file:
        questions = json.load(file)
    print("folder:", PATH, "| exists:", PATH.exists())
    print("everything inside:", list(PATH.rglob("*"))[:10])

    result = []
    t = build_index(ALL_FILES_PATH)


    while True :

        # source = []
        question = input("You >> ")
        if not question or question == "" :
            continue
        
        top_chunks = search(question, t, 5)
        if not top_chunks:
            raise "I don't Know!"
        else:
            test_question = "What activation formats does the fused batched MoE layer return in vLLM?"
        
            context = build_context(top_chunks)

            prompt = (
                "Answer in 1 to 3 sentences using only the context below. "
                "If the answer is not in the context, say you don't know.\n\n"
                f"Context:\n{context}\n\n"
                f"Question: {test_question} /no_think"
            )

            response = Client.chat(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0},
            )
            # print(response["message"]["content"])
            answer = response.message.content or ""
            answer = re.sub(r"<think>.*?</think>", "", answer, flags=re.DOTALL).strip()

            print(answer)

        # result.append(AnsweredQuestion(
        #     question_id = item["question_id"],
        #     question = question,
        #     sources = sources,
        #     answer = "",
        # ))

