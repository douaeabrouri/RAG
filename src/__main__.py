# from chunking.chunker import  ALL_FILES_PATH
# from indexing.bm25_ranking import search, build_index
# from pathlib import Path
# import json
# from managing_answers.save import save_answered, save_unanswered
# import sys
import fire
from src.commands import  CLI


# PATH = BASE_DIR / "data" / "datasets_public" / "public" / "UnansweredQuestions"
# FILE1 = PATH / "dataset_code_public.json"

# OUT_PATH = BASE_DIR / "data" / "output" / "search_results_and_answer" / "AnsweredQuestions"
# output_file = OUT_PATH / "dataset_code_public.json"
# output_file.parent.mkdir(parents=True, exist_ok=True)
# OUT_PATH1 = BASE_DIR / "data" / "output" / "search_results" / "AnsweredQuestions"
# output_file1 = OUT_PATH / "dataset_code_public.json"
# output_file1.parent.mkdir(parents=True, exist_ok=True)



# with open(FILE1, "r") as file:
#     questions = json.load(file) 


# t = build_index(ALL_FILES_PATH)
# searched = []
# chunks_by_id = {}
# for item in questions["rag_questions"]:
#     top_chunks = search(item["question"], t, K)
#     chunks_by_id[item["question_id"]] = top_chunks
#     searched.append(MinimalSearchResults(
#         question_id=item["question_id"],
#         question=item["question"],
#         retrieved_sources = to_source(top_chunks),
#     ))
#     if item["question"].lower() in EXIT_FILES :
#         sys.exit()

#     save_unanswered(searched, K, output_file1)

# answered = []
# for item in questions["rag_questions"]:
#     top_chunks = chunks_by_id[item["question_id"]]
#     if top_chunks:
#         answer = ask_llm(make_prompt(item["question"], top_chunks))
#     else:
#         answer =  "I don't Know!"
#         retrieved_sources = []

#     answered.append(MinimalAnswer(
#         question_id=item["question_id"],
#         question=item["question"],
#         retrieved_sources=to_source(top_chunks),
#         answer=answer,
#     ))
#     save_answered(answered, K, output_file)

    ##### Evaluation with recall@k must be here?

##### fix the command #####

if __name__ == "__main__":
    fire.Fire(CLI)

