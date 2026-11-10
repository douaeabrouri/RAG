from pathlib import Path
from ollama import Client

GREEN = "\033[0;32m"
RESET = "\033[0m"
RED = "\033[31m"
ALLOWED_FILES = [".py", ".md", ".txt"]
DEFAULT_MAX_CHUNK_SIZE = 2000
BASE_DIR = Path(__file__).resolve().parent
PATH = BASE_DIR / "data" / "raw" / "vllm-0.10.1"
OLLAM_HOST = "http://127.0.0.1:11434"
MODEL_NAME="qwen3:0.6b"
CLIENT = Client(host=OLLAM_HOST)
K = 3
PATH = BASE_DIR / "data" / "search_results_and_answer" / "UnansweredQuestions"
FILE1 = PATH / "dataset_code_public.json"
FILE2 = PATH / "dataset_docs_public.json"
LIST_OF_FILES = [FILE1, FILE2]
EXIT_FILES= ["bye", "exit", "quit", "q", "close"]