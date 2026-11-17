import json
import pickle
from pathlib import Path
from pydantic import ValidationError
from chunking.chunker import get_files_path
from constants import DEFAULT_MAX_CHUNK_SIZE, EXIT_FILES, GREEN, RED, RESET
from evaluation import evaluate_ssr
from indexing.bm25_ranking import build_index, search as search_chunks
from managing_answers.save import save_answered, save_unanswered
from src.answerdquestion import RagDataset
from src.ask_llm import ask_llm, to_source
from src.minimalsource import MinimalAnswer, MinimalSearchResults


class CLI:
    """Expose indexing, retrieval, answering, and evaluation commands."""

    def index(
        self,
        max_chunk_size: int = DEFAULT_MAX_CHUNK_SIZE,
        raw_data: str = "data/raw",
        processed_data: str = "data/processed",
    ) -> None:
        """Build and save a BM25 index from supported raw repository files.

        Args:
            max_chunk_size: Maximum number of characters per text chunk.
            raw_data: Directory containing the ``vllm-0.10.1`` source folder.
            processed_data: Directory where the index and chunk metadata are
                written.

        Returns:
            None. Status and errors are reported in the command-line output.
        """
        try:
            if not (0 < max_chunk_size <= DEFAULT_MAX_CHUNK_SIZE):
                print(
                    f"{RED}The chunk max size must be between 1 and "
                    f"{DEFAULT_MAX_CHUNK_SIZE}.{RESET}"
                )
                return
            try:
                raw = Path(raw_data) / "vllm-0.10.1"
                raw.mkdir(parents=True, exist_ok=True)
            except FileNotFoundError:
                print(f"{RED}ERROR:{RESET} File not found")
                return
            try:
                bm25, chunks = build_index(get_files_path(raw), max_chunk_size)
            except Exception as exc:
                print(f"{RED}ERROR: {exc}{RESET}")
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
            print(
                f"{GREEN}Ingestion complete! Indices saved under "
                f"data/processed/{RESET}"
            )
        except Exception as exc:
            print(f"{RED}ERROR: {exc}{RESET}")

    def search(self, query: str, k: int = 3) -> None:
        """Search the saved index and print matching source ranges.

        Args:
            query: Text to search for in the indexed chunks.
            k: Maximum number of results to display.

        Returns:
            None. Matching sources or an error are printed to the console.
        """
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

            result_of_query = search_chunks(query, bm25, chunks, k)
            if not result_of_query:
                print("There is no answere for this Query!")
                return
            for item in result_of_query:
                print(
                    f'{item["file_path"]} '
                    f'[{item["first_character_index"]}:'
                    f'{item["last_character_index"]}]'
                )
        except Exception as exc:
            print(f"{RED}ERROR: {exc}{RESET}")

    def answer(self, query: str, k: int = 3) -> None:
        """Retrieve relevant chunks and print a generated answer.

        Args:
            query: Question to answer using indexed source material.
            k: Maximum number of retrieved chunks to pass to the model.

        Returns:
            None. The answer or an error is printed to the console.
        """
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
        except Exception as exc:
            print(f"{RED}ERROR: {exc}{RESET}")

    def search_dataset(
        self,
        dataset_path: str,
        k: int,
        save_directory: str,
    ) -> None:
        """Run retrieval for every question in a dataset and save results.

        Args:
            dataset_path: JSON dataset containing RAG questions.
            k: Maximum number of chunks to retrieve per question.
            save_directory: Directory where the retrieval result file is
                written.

        Returns:
            None. Results are saved as questions are processed; errors are
            printed to the console.
        """
        try:
            if k <= 0:
                raise ValueError("The Value of K must be > 0")
            bm25, chunks = build_index(
                get_files_path(Path("data/raw/vllm-0.10.1"))
            )
            searched: list[MinimalSearchResults] = []

            with open(dataset_path, "r", encoding="utf-8") as file:
                questions = RagDataset.model_validate_json(file.read())

            for question in questions.rag_questions:
                top_chunks = search_chunks(question.question, bm25, chunks, k)
                searched.append(
                    MinimalSearchResults(
                        question_id=question.question_id,
                        question=question.question,
                        retrieved_sources=to_source(top_chunks),
                    )
                )
                if question.question.lower() in EXIT_FILES:
                    return
                out_dir = Path(save_directory)
                out_dir.mkdir(parents=True, exist_ok=True)
                out_file = out_dir / Path(dataset_path).name
                save_unanswered(searched, k, out_file)
            print(f"{GREEN}Saved student_search_results to {out_file}{RESET}")

        except FileNotFoundError:
            print(f"{RED}ERROR: Dataset file not found: {dataset_path}{RESET}")
        except ValidationError as exc:
            print(f"{RED}ERROR: Invalid dataset file: {exc}{RESET}")
        except Exception as exc:
            print(f"{RED}ERROR: {exc}{RESET}")

    def answer_dataset(
        self,
        student_search_results_path: str,
        save_directory: str,
    ) -> None:
        """Generate and save answers for previously retrieved dataset results.

        Args:
            student_search_results_path: JSON file containing questions and
                retrieved sources.
            save_directory: Existing directory where answered results are
                saved.

        Returns:
            None. Answered results are saved and errors are printed.

        Raises:
            FileNotFoundError: If either supplied path does not exist.
        """
        if not Path(student_search_results_path).exists():
            raise FileNotFoundError(
                f"Search results file not found: {student_search_results_path}"
            )
        try:
            with open(Path(student_search_results_path), "r") as file:
                questions = json.load(file)
            if not questions:
                raise ValueError("Empty file!!")
            answered: list[MinimalAnswer] = []
            for item in questions["search_results"]:
                retrieved_sources = item["retrieved_sources"]
                if retrieved_sources:
                    answer = ask_llm(item["question"], retrieved_sources)
                else:
                    answer = "I don't know!"
                answered.append(
                    MinimalAnswer(
                        question_id=item["question_id"],
                        question=item["question"],
                        retrieved_sources=retrieved_sources,
                        answer=answer,
                    )
                )
                save_path = Path(save_directory)
                if save_path.suffix.lower() == ".json":
                    save_path.parent.mkdir(parents=True, exist_ok=True)
                    out_file = save_path
                else:
                    save_path.mkdir(parents=True, exist_ok=True)
                    out_file = save_path / Path(student_search_results_path).name
                save_answered(answered, questions["k"], out_file)
            print(
                f"{GREEN}Saved student_search_results_and_answer to "
                f"{out_file}{RESET}"
            )
        except Exception as exc:  # pragma: no cover - CLI error path
            print(f"{RED}ERROR: {exc}{RESET}")

    def evaluate_search_results(
        self,
        student_path: str,
        dataset_path: str,
        k: int = 5,
    ) -> None:
        """Evaluate saved retrieval results against a reference dataset.

        Args:
            student_path: JSON file containing the student's search results.
            dataset_path: JSON file containing reference questions and sources.
            k: Highest retrieval rank to evaluate.

        Returns:
            None. Evaluation metrics or errors are printed to the console.
        """
        try:
            if not (
                Path(student_path).exists() and Path(dataset_path).exists()
            ):
                raise FileNotFoundError(
                    "One or both input paths do not exist."
                )
            if not 0 < k:
                raise ValueError("The value of k must be positive.")
            evaluate_ssr(student_path, dataset_path, k)
        except Exception as exc:
            print(f"{RED}ERROR: {exc}{RESET}")
