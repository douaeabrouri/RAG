
import pickle, json
from pathlib import Path
from chunking.chunker import get_files_path
from indexing.bm25_ranking import search as search_chunks
from indexing.bm25_ranking import build_index, load_index
from src.ask_llm import ask_llm, to_source
from src.build_context import build_context
from managing_answers.save import save_unanswered, save_answered
from src.minimalsource import MinimalSearchResults, MinimalAnswer
from constants import EXIT_FILES 

class CLI:

    def index(self, max_chunk_size: int = 2000, 
              raw_data: str = "data/raw",
              processed_data: str = "data/processed") -> None:

        try:
            if not (0 <= max_chunk_size <= 2000):
                print("The chunk maxe size must be positive and > 0!")
                return 
            try:
                raw = Path(raw_data + "/vllm-0.10.1") 
                raw.mkdir(parents=True, exist_ok=True)
            except FileNotFoundError:
                print("ERROR: FIle not found")
                return 
            try:
                bm25, chunks = build_index(get_files_path(raw))
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
                    "first_charactere_index": str(chunk.first_char_index),
                    "last_charactere_index": str(chunk.last_char_index), 
                }
                chunks_metadata.append(metadata)
            with (processed / "chunks.json").open("w") as file:
                json.dump(chunks_metadata, file, indent=2)
            print("\nIngestion complete! Indices saved under data/processed/\n")
        except Exception as e:
            print(f"ERROR: {e}")

    def search(self, query: str, K: int = 3) -> None:

        try:
            processed_path = Path("data/processed")
            chunks_path = processed_path / "chunks.json"
            bm25_path = processed_path / "index.pkl"
        
            if not query:
                raise ValueError("The query cannot be empty.")
            if 0 >= K :
                raise ValueError("The Value of K must be > 0")
            with bm25_path.open("rb") as file:
                bm25 = pickle.load(file)
            with chunks_path.open("r") as file:
                chunks = json.load(file)

            result_of_query = search_chunks(query, bm25, chunks ,K)
            if not result_of_query:
                print("There is no answere for this Query!")
                return
            for item in result_of_query:
                print(f'{item["file_path"]} [{item["first_charactere_index"]}:{item["last_charactere_index"]}]')
        except Exception as e:
            print(f"ERROR: {e}")

    def answer(self, query: str, K: int = 3):
        try:
            processed_path = Path("data/processed")
            chunks_path = processed_path / "chunks.json"
            bm25_path = processed_path / "index.pkl"
        
            if not query:
                raise ValueError("The query cannot be empty.")
            if 0 >= K :
                raise ValueError("The Value of K must be > 0")
            with bm25_path.open("rb") as file:
                bm25 = pickle.load(file)
            with chunks_path.open("r") as file:
                chunks = json.load(file)

            top_chunks = search_chunks(query, bm25, chunks, K)
            answer = ask_llm(query, top_chunks)
            print(answer)
        except Exception as e:
            print(f"ERROR: {e}")

    def search_dataset(self, dataset_path: str, K: int, save_directory: str):

        try:
            bm25, chunks = build_index(get_files_path(Path("data/raw/vllm-0.10.1")))
            searched = []
            chunks_by_id = {}

            with open(dataset_path, "r") as file:
                questions = json.load(file)

            for item in questions["rag_questions"]:
                top_chunks = search_chunks(item["question"], bm25, chunks, K)
                chunks_by_id[item["question_id"]] = top_chunks
                searched.append(MinimalSearchResults(
                    question_id=item["question_id"],
                    question=item["question"],
                    retrieved_sources = to_source(top_chunks),
                ))
                if item["question"].lower() in EXIT_FILES :
                    return
                out_dir = Path(save_directory)
                out_dir.mkdir(parents=True, exist_ok=True)

                out_file = out_dir / Path(dataset_path).name

                save_unanswered(searched, K, out_file)

        except Exception as e:
            print(f"ERROR: {e}")

    def answer_dataset(self, student_search_results_path: str, save_directory: str):

        try:
            with open(student_search_results_path, "r") as file:
                questions = json.load(file)

            if not questions:
                raise ValueError("Empty file!!")
            
            answered = []
            chunks_by_id = {}

            print(questions["K"])
            # for item in questions["search_results"]:
                # top_chunks = chunks_by_id[item["question_id"]]
                # if top_chunks:
                #     answer = ask_llm(item["question"], top_chunks)
                # else:
                #     answer =  "I don't Know!"                
                # answered.append(MinimalAnswer(
                #     question_id=item["question_id"],
                #     question=item["question"],
                #     retrieved_sources=to_source(top_chunks),
                #     answer=answer,
                # ))
                # save_answered(answered, K, save_directory)
            
        except Exception as e:
            print(f"ERROR: {e}")  
