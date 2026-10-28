
import pickle
from pathlib import Path
from chunking.chunker import get_files_path
from indexing.bm25_ranking import build_index


class CLI():
    def index(self, max_chunk_size: int = 2000, 
              raw_data: str = "data/raw",
              processed_data: str = "data/processed") -> None:

        if not (0 < max_chunk_size <= 2000):
            print("The chunk maxe size must be positive and > 0!")
            return 
        try:
            raw = Path(raw_data + "/vllm-0.10.1") 
            raw.mkdir(parents=True, exist_ok=True)
        except FileNotFoundError:
            print("ERROR: FIle not found")
            return 
        try:
            t = build_index(get_files_path(raw))
        except Exception as e:
            print(f"ERROR: {e}")
            return
    
        processed = Path(processed_data)
        processed.mkdir(parents=True, exist_ok=True)
        with (processed / "index.pkl").open("wb") as file:
            pickle.dump(t, file)
        print("\nIngestion complete! Indices saved under data/processed/\n")

