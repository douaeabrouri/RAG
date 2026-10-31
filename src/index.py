
import pickle, json
from pathlib import Path
from chunking.chunker import get_files_path
from indexing.bm25_ranking import search as search_chunks
from indexing.bm25_ranking import build_index, load_index


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

    def search(self, query: str, K: int = 3):

        processed_path = Path("data/processed")
        chunks_path = processed_path / "chunks.json"
        bm25_path = processed_path / "index.pkl"
    
        if 0 >= K :
            raise ValueError("The Value of K must be > 0")
        with bm25_path.open("r") as file:
            bm25 = pickle.load(file)
        print("Hey")
        with chunks_path.open("r") as file:
            chunks = json.load(file)

        result_of_query = search_chunks(query, bm25, chunks ,K)
        print(result_of_query)

    


        