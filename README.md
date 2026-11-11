*This project has been created as part of the 42 curriculum by doabrour.*

# RAG — Retrieval-Augmented Generation

## Description

**RAG (Retrieval-Augmented Generation)** is a project that explores how to build a system capable of answering questions about a codebase using its source code and documentation.

The goal is to combine information retrieval with a Large Language Model (LLM). Instead of asking an LLM to answer questions using only its internal knowledge, the system first retrieves relevant parts of a given repository and then provides those parts as context to the model.

In this project, the system works with the **vLLM 0.10.1** codebase. It retrieves relevant code or documentation chunks using the BM25 ranking algorithm and uses **Qwen3-0.6B** to generate answers based on the retrieved context.

The project also includes an evaluation process to measure retrieval quality using Recall@k.

### Main features

- Index Python, Markdown, and text files.
- Split files into smaller chunks while preserving their source locations.
- Retrieve relevant chunks using BM25.
- Generate context-based answers using an LLM.
- Evaluate retrieval quality against reference datasets.
- Provide a command-line interface to run the different operations.

## System Architecture

The project follows a Retrieval-Augmented Generation pipeline composed of several stages.

```text
                 vLLM 0.10.1 Repository
                           |
                           v
                    File Discovery
                           |
                           v
                      Chunking
             +-------------+-------------+
             |             |             |
          Python        Markdown        Text
          AST           Recursive       Recursive
          Chunker       Splitter        Splitter
             |             |             |
             +-------------+-------------+
                           |
                           v
                    BM25 Indexing
                           |
                           v
                     User Question
                           |
                           v
                    BM25 Retrieval
                           |
                           v
                  Top-K Relevant Chunks
                           |
                           v
                    Context Building
                           |
                           v
                    Qwen3-0.6B LLM
                           |
                           v
                     Generated Answer
```

### Pipeline components

1. **File discovery**

   The system searches the repository for supported file types: `.py`, `.md`, and `.txt`.

2. **Chunking**

   Each file is divided into smaller pieces. The chunking method depends on the file type.

3. **Indexing**

   The generated chunks are tokenized and indexed using BM25.

4. **Retrieval**

   When a question is submitted, the system calculates a BM25 relevance score for each indexed chunk and selects the top-K results.

5. **Context building**

   The retrieved chunks are reconstructed from their original files using their character offsets. Their file paths are included in the context.

6. **Answer generation**

   The question and retrieved context are sent to Qwen3-0.6B through Ollama. The model is instructed to answer using only the provided context.

7. **Evaluation**

   Retrieved sources can be compared with the ground-truth sources to calculate Recall@k.

## Chunking Strategy

Chunking is an important part of a RAG system because retrieving an entire file is often inefficient. Smaller, meaningful sections make it easier to locate relevant information.

This project uses different strategies depending on the file format.

### Python files

Python files are processed using Python's built-in `ast` module.

- The source code is parsed into an Abstract Syntax Tree (AST).
- The system examines top-level nodes such as classes and functions.
- Nodes that fit within the maximum chunk size are kept together.
- Oversized nodes are recursively divided into their child nodes when possible.
- Long sections that cannot be divided structurally are split into smaller pieces.
- The resulting pieces are packed into chunks without exceeding the configured maximum constant.

This approach attempts to preserve the logical structure of Python code.

If a Python file cannot be parsed because of a syntax error, the text chunking strategy is used as a fallback.

### Markdown and text files

Markdown and text files use `RecursiveCharacterTextSplitter` from LangChain.

The current configuration uses:

- Maximum chunk size: **2000 characters**
- Chunk overlap: **200 characters**
- Start-index tracking: enabled

The overlap helps preserve information that might otherwise be lost when a relevant passage is located near a chunk boundary.

### Source metadata

Each chunk stores metadata that allows the system to identify its original location:

- File path
- First and last line
- First character index
- Last character index

This metadata is important for retrieval evaluation and for reconstructing the original context.

## Retrieval Method

The project uses **BM25 (Best Matching 25)**, a lexical information retrieval algorithm.

BM25 ranks documents according to how relevant their terms are to a search query. It considers factors such as term frequency, inverse document frequency, and document length.

### Indexing

The system:

1. Collects chunks from supported files.
2. Extracts their text.
3. Converts text into lowercase tokens.
4. Builds a BM25 index using `BM25Okapi` from the `rank-bm25` library.

### Search and ranking

When a user submits a question:

1. The question is converted into lowercase tokens.
2. BM25 calculates a relevance score for every indexed chunk.
3. The chunks are sorted by score in descending order.
4. The system returns up to the requested K highest-ranked chunks.
5. Chunks with a score less than or equal to zero are ignored.

The value of K determines how many retrieved chunks are passed to the next stage.

### Why BM25?

BM25 was selected because it is a lightweight and well-established retrieval method. It does not require training a neural embedding model and provides a useful baseline for searching source code and documentation.

One limitation is that BM25 relies on lexical similarity. It may fail to retrieve relevant content when a question uses different terminology from the source code.

## Answer Generation

After retrieval, the system builds a context from the selected chunks.

The context contains the original source text and its file path. This context is passed to the LLM along with the user's question.

The project uses:

- **Model:** Qwen3-0.6B
- **Runtime:** Ollama
- **Temperature:** 0

The prompt instructs the model to:

- Answer using only the provided context.
- Keep answers between one and three sentences.
- Preserve identifiers exactly as they appear in the source.
- Avoid using external knowledge.
- Say that it does not know when the context contains no relevant information.

This approach helps reduce unsupported answers.

## Performance Analysis

Retrieval quality is evaluated using **Recall@k**.

Recall@k measures how many relevant reference sources are retrieved within the first k results.

A retrieved source is considered relevant when:

- Its file path matches the reference source.
- Its character-offset intervals overlap sufficiently.
- The Intersection over Union (IoU) of the intervals is at least 0.05.

The project evaluation uses the following official thresholds:

| Dataset | Required metric | Minimum score |
|---|---:|---:|
| Documentation | Recall@5 | 80% |
| Code | Recall@5 | 50% |

Recall@1, Recall@3, and Recall@10 can also be useful for understanding how retrieval ranking changes as K increases.

### Performance considerations

The project also considers:

- Indexing time.
- Retrieval time across the evaluation questions.
- The number of retrieved chunks.
- The maximum size of the context provided to the LLM.

The final indexing and retrieval timings should be measured on the machine used for evaluation and added here.

## Design Decisions

### Different chunking strategies

Python code has a structural organization that can be explored through its AST. Markdown and text files are better handled through recursive character splitting.

Using different chunking methods allows the project to account for these differences.

### Character offsets

The project stores character offsets rather than only storing chunk text. This makes it possible to reconstruct the original source passages and compare retrieved chunks against the ground-truth intervals.

### BM25 instead of embeddings

BM25 provides a straightforward baseline without requiring an embedding model or vector database. It also makes the retrieval process easier to inspect and debug.

### Separate retrieval and generation

The project separates retrieving information from generating answers. This makes it possible to evaluate retrieval independently of the LLM's answer quality.

### Pydantic models

Pydantic models are used to represent chunks and search-result data with explicit types and structured fields.

### Command-line interface

The project uses Python Fire to expose its operations through a command-line interface.

## Challenges Faced

### Choosing the right chunk size

Chunks that are too large may contain irrelevant information, while chunks that are too small may lose important context.

The project uses a maximum of 2000 characters and a 200-character overlap for Markdown and text splitting.

### Preserving source locations

Retrieval evaluation depends on identifying the exact location of a relevant passage.

For this reason, the chunking process stores file paths and character offsets, allowing the system to compare retrieved passages with reference sources.

### Improving code retrieval

Code retrieval is challenging because identifiers can be written in different styles, and questions do not always use exactly the same words as the source code.

Experiments with tokenization and ranking are important for improving Recall@5.

### Evaluating retrieval separately from answers

A generated answer can sound correct even when the system retrieves the wrong source. Evaluating Recall@k separately helps identify problems in the retrieval stage before investigating answer generation.

## Instructions

### Requirements

- Python 3.10 or later
- [uv](https://docs.astral.sh/uv/)
- [Ollama](https://ollama.com/)

### Installation

Clone the repository:

```bash
git clone https://github.com/douaeabrouri/RAG.git
cd RAG
```

Install the Python dependencies using uv:

```bash
uv sync
```

Pull the Qwen model:

```bash
ollama pull qwen3:0.6b
```

Make sure the Ollama service is running before using the answer-generation commands.

### Build the index

Run:

```bash
uv run python -m src index
```

The index and chunk metadata are saved in:

```text
data/processed/
├── index.pkl
└── chunks.json
```

### Search for relevant chunks

Run a search with a question:

```bash
uv run python -m src search \
    --query="How does the attention mechanism work?" \
    --k=5
```

### Generate an answer

Run:

```bash
uv run python -m src answer \
    --query="How does the attention mechanism work?" \
    --k=5
```

The system retrieves the top five chunks and sends their context to Qwen3-0.6B.

### Search an evaluation dataset

For example, to search the code questions:

```bash
uv run python -m src search_dataset \
    --dataset_path="data/datasets/UnansweredQuestions/dataset_code_public.json" \
    --k=5 \
    --save_directory="data/output/search_results"
```

For documentation questions:

```bash
uv run python -m src search_dataset \
    --dataset_path="data/datasets/UnansweredQuestions/dataset_docs_public.json" \
    --k=5 \
    --save_directory="data/output/search_results"
```

### Generate answers for a dataset

After generating search results, run:

```bash
uv run python -m src answer_dataset \
    --student_search_results_path="data/output/search_results/dataset_code_public.json" \
    --save_directory="data/output/search_results_and_answer"
```

### Evaluate retrieval results

Evaluate the code dataset:

```bash
uv run python -m src evaluate_search_results \
    --student_path="data/output/search_results/dataset_code_public.json" \
    --dataset_path="data/datasets/AnsweredQuestions/dataset_code_public.json" \
    --k=5
```

Evaluate the documentation dataset:

```bash
uv run python -m src evaluate_search_results \
    --student_path="data/output/search_results/dataset_docs_public.json" \
    --dataset_path="data/datasets/AnsweredQuestions/dataset_docs_public.json" \
    --k=5
```

The evaluation command compares the retrieved sources with the ground-truth sources and reports the retrieval score.

## Resources

### Documentation and references

- [BM25 — Introduction and explanation](https://en.wikipedia.org/wiki/Okapi_BM25)
- [rank-bm25 documentation](https://github.com/dorianbrown/rank_bm25)
- [Python Abstract Syntax Trees (AST)](https://docs.python.org/3/library/ast.html)
- [LangChain Text Splitters](https://docs.langchain.com/oss/python/integrations/splitters)
- [Python Fire documentation](https://github.com/google/python-fire)
- [Ollama documentation](https://docs.ollama.com/)
- [Qwen3 model](https://ollama.com/library/qwen3)

### AI usage

AI tools, They were used for:

- Understanding RAG concepts, BM25, chunking, retrieval, and Recall@k.
