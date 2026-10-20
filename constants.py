from pathlib import Path


ALLOWED_FILES = [".py", ".md", ".txt"]
MAX_CHARS = 2000
BASE_DIR = Path(__file__).resolve().parent
PATH = BASE_DIR / "vllm_tester"
OLLAM_HOST="http://10.30.236.180:11434"
MODEL_NAME="qwen3:0.6b"