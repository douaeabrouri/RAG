from pathlib import Path
from src.answerdquestion import AnsweredQuestion, RagDataset
from src.search_result import StudentSearchResults

def iou(start1, end1, start2, end2):
    intersection = max(0, min(end1, end2) - max(start1, start2))
    union = (end1 - start1) + (end2 - start2) - intersection
    if union <= 0:
        return 0.0
    iou = intersection / union
    return iou

def found(file1, file2, ar1 ,ar2, threshold=0.05) -> bool:
    if file1 != file2:
        return False
    return iou(ar1[0], ar1[1], ar2[0], ar2[1]) >= threshold

def evaluate_ssr(student_path, dataset_path, k):

    if k <= 0:
        raise ValueError("k must be positive")

    student = StudentSearchResults.model_validate_json(
        Path(student_path).read_text(encoding="utf-8")
    )

    dataset = RagDataset.model_validate_json(
        Path(dataset_path).read_text(encoding="utf-8")
    )

    results = student.search_results

    truth_by_id = {
        question.question_id: question.sources
        for question in dataset.rag_questions
        if isinstance(question, AnsweredQuestion)
        and question.sources
    }
    student_by_id = {}
    for result in results:
        if result.question_id in student_by_id:
            raise ValueError(
                f"Duplicate question ID: {result.question_id}"
            )
        student_by_id[result.question_id] = result
    with_rs = sum(
        1 for result in results if result.retrieved_sources
    )
    recall_results = {}
    for i in range(1, k + 1):
        scores = []
        for question_id, truths in truth_by_id.items():
            student_result = student_by_id.get(question_id)
            if student_result is None:
                scores.append(0.0)
                continue
            retrieved = student_result.retrieved_sources[:i]
            hits = 0
            for truth in truths:
                for source in retrieved:
                    if found(
                        truth.file_path,
                        source.file_path,
                        (
                            truth.first_character_index,
                            truth.last_character_index,
                        ),
                        (
                            source.first_character_index,
                            source.last_character_index,
                        ),
                    ):
                        hits += 1
                        break
            scores.append(hits / len(truths))
        if not scores:
            raise ValueError("No answered questions with ground truth.")
        recall = sum(scores) / len(scores)
        recall_results[i] = recall
        successful = sum(1 for score in scores if score == 1.0)
        failed = sum(1 for score in scores if score == 0.0)
        print(f"\nEvaluation Results (Recall@{i})")
        print("=" * 40)
        print(f"Student questions: {len(results)}")
        print(f"Questions with retrieved sources: {with_rs}")
        print(f"Answered questions evaluated: {len(scores)}")
        print(f"Successful retrievals: {successful}")
        print(f"Failed retrievals: {failed}")
        print(f"Recall: {recall * 100:.2f}%")
    return recall_results
                    
