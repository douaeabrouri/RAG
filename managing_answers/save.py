from src.search_result import StudentSearchResultsAndAnswer, StudentSearchResults
import json


def save_unanswered(result, k, path) -> None:
    try:
        output = StudentSearchResults(search_results=result, k=k)
        with open(path, "w") as file:
            json.dump(output.model_dump(mode='json'), file, indent=3, ensure_ascii=False)
    except Exception as e:
        print(e)
        return

def save_answered(result, k, path) -> None:
    try:
        output = StudentSearchResultsAndAnswer(search_results=result, k=k)
        with open(path, "w") as file:
            json.dump(output.model_dump(mode="json"), file, indent=3, ensure_ascii=False)
    except Exception as e:
        print(e)
        return
