from pathlib import Path
import json

def iou(start1, end1, start2, end2):
    intersection = max(0, min(end1, end2) - max(start1, start2))
    union = (end1 - start1) + (end2 - start2) - intersection    
    iou = intersection / union
    return iou

def found(file1, file2, ar1 ,ar2, threshold=0.05) -> bool:
    if file1 != file2:
        return False
    return iou(ar1[0], ar1[1], ar2[0], ar2[1]) >= threshold

def evaluate_ssr(student_path, dataset_path, k):

    with open(Path(student_path), "r") as file:
        student = json.load(file)

    with open(Path(dataset_path), "r") as file:
        dataset = json.load(file)
    
    try:
        results = student["search_results"]
        with_rs = sum(1 for r in results if r["retrieved_sources"])
        with_or_without_rs = sum(1 for r in results)
        truth_by_id = {q["question_id"]: q["sources"] for q in dataset["rag_questions"]}
        valid = True
    except (KeyError, TypeError):
        print("Student data is valid: False")
        return

    scores = []
    for item in student["search_results"]:
        truths = truth_by_id.get(item["question_id"])
        if not truths:
            continue
        if "retrieved_sources" not in item:
            continue
        retrieved = item["retrieved_sources"][:k]
        hits = 0
        for t in truths:
            for r in retrieved:
                if found(
                    t["file_path"], r["file_path"],
                    (t["first_character_index"], t["last_character_index"]),
                    (r["first_character_index"], r["last_character_index"]),
                ):
                    hits += 1
                    break
        scores.append(hits / len(truths))
    print("evaluaion result:\n")
    recall = 0.0
    if not scores:
        print("Maybe you compare the wrong files, check your input!")
        return 
    recall = sum(scores) / len(scores)
    print(f"Student data is valid: {valid}")
    print(f"Total number of questions with student sources: {with_rs}")
    print(f"Total number of questions: {len(truth_by_id)}\n")
    print("Evaluation Results")
    print("========================================")
    print(f"Questions evaluated: {with_or_without_rs}")

    recall = sum(scores) / len(scores)
    print(f"{(recall*100)}%")

    return recall
                    


