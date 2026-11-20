from src.search_result import (
    StudentSearchResultsAndAnswer,
    StudentSearchResults,
)
import json


def save_unanswered(result, k, path) -> None:
    """Serialize retrieval results without generated answers to JSON.

    Args:
        result: Search-result records to serialize.
        k: Number of top results requested per question.
        path: Destination JSON file path.

    Returns:
        None. Serialization errors are printed and suppressed.
    """
    try:
        output = StudentSearchResults(search_results=result, k=k)
        with open(path, "w") as file:
            json.dump(
                output.model_dump(mode='json'),
                file,
                indent=3,
                ensure_ascii=False
            )
    except Exception as e:
        print(e)
        return


def save_answered(result, k, path) -> None:
    """Serialize retrieval results and generated answers to JSON.

    Args:
        result: Answered search-result records to serialize.
        k: Number of top results requested per question.
        path: Destination JSON file path.

    Returns:
        None. Serialization errors are printed and suppressed.
    """
    try:
        output = StudentSearchResultsAndAnswer(search_results=result, k=k)
        with open(path, "w") as file:
            json.dump(
                output.model_dump(mode="json"),
                file,
                indent=3,
                ensure_ascii=False
            )
    except Exception as e:
        print(e)
        return
