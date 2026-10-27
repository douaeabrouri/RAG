from constants import BASE_DIR
from src.search_result import StudentSearchResultsAndAnswer, StudentSearchResults
import json

OUT_PATH = BASE_DIR / "data" / "search_results_and_answer" / "AnsweredQuestions"
output_file = OUT_PATH / "dataset_code_public.json"
output_file.parent.mkdir(parents=True, exist_ok=True)


def save_answered(result, k, path) -> None:
    output = StudentSearchResultsAndAnswer(search_results=result, k=k)
    with open(path, "w") as file:
        json.dump(output.model_dump(mode="json"), file, indent=3, ensure_ascii=False)


def save_unanswered(result, k, path) -> None:
    output = StudentSearchResults(search_results=result, k=k)
    with open(path, "w") as file:
        json.dump(output.model_dump(mode='json'), file, indent=3, ensure_ascii=False)