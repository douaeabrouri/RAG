from pathlib import Path
import json

def iou(start1, end1, start2, end2):
    intersection = (0, min(end1, end2) - max(start1, start2))
    union = start1 - end2
    iou = intersection / union
    return iou

def found(file1, file2, ar1 ,ar2, threshold=0.05) -> bool:
    if file1 != file2:
        return False
    return iou(ar1[0], ar1[1], ar2[0], ar2[1]) >= threshold

def evaluate_ssr(student_path, dataset_path, K):
    with open(Path(student_path), "r") as file:
        student = json.load(file)

    with open(Path(dataset_path), "r") as file:
        dataset = json.load(file)
    
    truth_by_id = {q["question_id"]: q["sources"] for q in dataset["rag_questions"]}

    scores = []
    for item in student["search_results"]:
        truths = truth_by_id.get(item["question_id"])
        if not truths:
            continue
        retrieved = item["retrieved_sources"][:K]

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

    recall = sum(scores) / len(scores) if scores else 0.0
    print(f"Recall@{K}: {recall:.2%} over {len(scores)} questions")
    return recall
                    


