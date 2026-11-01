# from chunking.chunker import  ALL_FILES_PATH
# from indexing.bm25_ranking import search, build_index
# from pathlib import Path
# import json
# from managing_answers.save import save_answered, save_unanswered
# import sys
import fire
from src.commands import  CLI

##### Evaluation with recall@k must be here?

if __name__ == "__main__":
    fire.Fire(CLI)

