from pathlib import Path
from ollama import Client


ALLOWED_FILES = [".py", ".md", ".txt"]
MAX_CHARS = 2000
BASE_DIR = Path(__file__).resolve().parent
PATH = BASE_DIR / "vllm_tester"
OLLAM_HOST = "http://127.0.0.1:11434"
MODEL_NAME="qwen3:0.6b"
Client = Client(host=OLLAM_HOST)