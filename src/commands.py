
import pickle, json
from pathlib import Path
from pydantic import ValidationError
from constants import DEFAULT_MAX_CHUNK_SIZE, EXIT_FILES, RED , RESET, GREEN
from chunking.chunker import get_files_path
from indexing.bm25_ranking import search as search_chunks
from indexing.bm25_ranking import build_index, load_index
from src.ask_llm import ask_llm, to_source
from src.build_context import build_context
from managing_answers.save import save_unanswered, save_answered
from src.minimalsource import MinimalSearchResults, MinimalAnswer
from src.answerdquestion import RagDataset
from evaluation import evaluate_ssr

class CLI:

    def index(self, max_chunk_size: int = DEFAULT_MAX_CHUNK_SIZE, 
              raw_data: str = "data/raw",
              processed_data: str = "data/processed") -> None:

        try:
            if not (0 < max_chunk_size <= DEFAULT_MAX_CHUNK_SIZE):
                print(f"The chunk max size must be between 1 and {DEFAULT_MAX_CHUNK_SIZE}.")
                return
            try:
                raw = Path(raw_data + "/vllm-0.10.1") 
                raw.mkdir(parents=True, exist_ok=True)
            except FileNotFoundError:
                print("ERROR: FIle not found")
                return
            try:
                bm25, chunks = build_index(get_files_path(raw), max_chunk_size)
            except Exception as e:
                print(f"ERROR: {e}")
                return
            processed = Path(processed_data)
            processed.mkdir(parents=True, exist_ok=True)
            with (processed / "index.pkl").open("wb") as file:
                pickle.dump(bm25, file)
            chunks_metadata = []
            for chunk in chunks:
                metadata = {
                    "file_path": str(chunk.file_path),
                    "first_character_index": str(chunk.first_character_index),
                    "last_character_index": str(chunk.last_character_index), 
                }
                chunks_metadata.append(metadata)
            with (processed / "chunks.json").open("w") as file:
                json.dump(chunks_metadata, file, indent=2)
            print("Ingestion complete! Indices saved under data/processed/")
        except Exception as e:
            print(f"{RED}ERROR: {e}{RESET}")

    def search(self, query: str, k: int = 3) -> None:

        try:
            processed_path = Path("data/processed")
            chunks_path = processed_path / "chunks.json"
            bm25_path = processed_path / "index.pkl"
        
            if not query:
                raise ValueError("The query cannot be empty.")
            if k <= 0 :
                raise ValueError("The Value of K must be > 0")
            with bm25_path.open("rb") as file:
                bm25 = pickle.load(file)
            with chunks_path.open("r") as file:
                chunks = json.load(file)

            result_of_query = search_chunks(query, bm25, chunks ,k)
            if not result_of_query:
                print("There is no answere for this Query!")
                return
            for item in result_of_query:
                print(f'{item["file_path"]} [{item["first_character_index"]}:{item["last_character_index"]}]')
        except Exception as e:
            print(f"{RED}ERROR: {e}{RESET}")

    def answer(self, query: str, k: int = 3):
        try:
            processed_path = Path("data/processed")
            chunks_path = processed_path / "chunks.json"
            bm25_path = processed_path / "index.pkl"
        
            if not query:
                raise ValueError("The query cannot be empty.")
            if k <= 0:
                raise ValueError("The Value of K must be > 0")
            with bm25_path.open("rb") as file:
                bm25 = pickle.load(file)
            with chunks_path.open("r") as file:
                chunks = json.load(file)

            top_chunks = search_chunks(query, bm25, chunks, k)
            answer = ask_llm(query, top_chunks)
            print(f"{GREEN}Answer:{RESET} {answer}")
        except Exception as e:
            print(f"{RED}ERROR: {e}{RESET}")

    def search_dataset(self, dataset_path: str, k: int, save_directory: str):

        try:
            if k <= 0:
                raise ValueError("The Value of K must be > 0")
            bm25, chunks = build_index(get_files_path(Path("data/raw/vllm-0.10.1")))
            searched = []
            chunks_by_id = {}

            with open(dataset_path, "r", encoding="utf-8") as file:
                questions = RagDataset.model_validate_json(file.read())

            for question in questions.rag_questions:
                top_chunks = search_chunks(question.question, bm25, chunks, k)
                chunks_by_id[question.question_id] = top_chunks
                searched.append(MinimalSearchResults(
                    question_id=question.question_id,
                    question=question.question,
                    retrieved_sources = to_source(top_chunks),
                ))
                if question.question.lower() in EXIT_FILES :
                    return
                out_dir = Path(save_directory)
                out_dir.mkdir(parents=True, exist_ok=True)
                out_file = out_dir / Path(dataset_path).name
                save_unanswered(searched, k, out_file)

        except FileNotFoundError:
            print(f"{RED}ERROR: Dataset file not found: {dataset_path}{RESET}")
        except ValidationError as e:
            print(f"{RED}ERROR: Invalid dataset file: {e}{RESET}")
        except Exception as e:
            print(f"{RED}ERROR: {e}{RESET}")

    def answer_dataset(self, student_search_results_path: str, save_directory: str):

        if not (Path(student_search_results_path).exists() and Path(save_directory).exists()):
            raise FileNotFoundError("One or both input paths do not exist.")
        try:
            with open(Path(student_search_results_path), "r") as file:
                questions = json.load(file)
            if not questions:
                raise ValueError("Empty file!!")
            answered = []
            for item in questions["search_results"]:
                retrieved_sources = item["retrieved_sources"]
                if retrieved_sources:
                    answer = ask_llm(item["question"], retrieved_sources)
                else:
                    answer =  "I don't Know!"                
                answered.append(MinimalAnswer(
                    question_id=item["question_id"],
                    question=item["question"],
                    retrieved_sources=to_source(retrieved_sources),
                    answer=answer,
                ))
                out_dir = Path(save_directory)
                out_dir.mkdir(parents=True, exist_ok=True)
                out_file = out_dir / Path(student_search_results_path).name
                save_answered(answered, questions["k"], out_file)
            
        except Exception as e:
            print(f"{RED}ERROR: {e}{RESET}")

    def evaluate_search_results(self, student_path: str, dataset_path: str, k: int = 5):
        try:
            if not (Path(student_path).exists() and Path(dataset_path).exists()):
                raise FileNotFoundError("One or both input paths do not exist.")
            if not 0 < k:
                raise ValueError("The value of k must be positive.")
            evaluate_ssr(student_path, dataset_path, k)
        except Exception as e:
            print(f"{RED}ERROR: {e}{RESET}")
