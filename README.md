# AccuKnox AI/ML Assessment

Submission for the AI/ML position assessment: three Python tasks (Assignment 1), written answers on LLM chatbots and vector databases (Assignment 2), and links to my most complex Python and database work.

## Repository contents

```
.
├── README.md
├── requirements.txt
├── task1_books_api.py                 # REST API -> SQLite -> display (books)
├── task2_scores_chart.py                 # Streaming API -> average -> bar chart (test scores)
├── task3_csv_import.py                 # CSV -> SQLite (users)
├── users.csv                # Sample input for Task 3
├── scores.png               # Output chart from Task 2
└── LLM_Chatbots_and_Vector_Databases_Assignment.docx   # Assignment 2 answers
```

## Setup

Requires Python 3.9+.

```
pip install -r requirements.txt
```

Run each task from the repository folder:

```
python task1_books_api.py
python task2_scores_chart.py
python task3_csv_import.py
```

## Assignment 1

### Task 1: API data retrieval and storage
Fetches a list of books (title, author, first publication year) from the Open Library search API, stores them in a local SQLite database (`books.db`), and prints them.

- The `books` table has a `UNIQUE(title, author)` constraint and inserts use `INSERT OR IGNORE`, so re-running the script does not create duplicates.
- Requests use a timeout and `raise_for_status()`; missing fields fall back to defaults ("Unknown" author, `NULL` year).
- SQL uses parameterized queries.

### Task 2: Data processing and visualization
Fetches student test scores from `https://live-test-scores.herokuapp.com/scores`, calculates the average, and draws a bar chart (`scores.png`).

- This endpoint is a **Server-Sent Events (SSE) stream**, not a plain JSON array. The script reads it line by line, keeps lines starting with `data:`, and parses the JSON.
- Because a stream may not end, reading stops after 2,000 events or 20 seconds, whichever comes first. The result therefore depends on how much data arrived in that window. On my run: 80 scores from 20 students, overall average 74.75%. Figures can vary slightly between runs.
- Scores arrive as fractions (0 to 1) and are converted to percentages.
- The chart shows one bar per student (their average across received exams) with a dashed line for the overall average, since plotting every score would be unreadable.

### Task 3: CSV import to a database
Reads `users.csv` (columns `name,email`) and inserts the rows into a SQLite database (`users.db`).

- Rows missing a name or email are skipped.
- Emails are stripped and lowercased before insertion, and `email` is `UNIQUE`, so `Alice@x.com` and `alice@x.com` are treated as the same user.
- The script prints how many rows were actually inserted. Running it a second time inserts 0 rows.

### Task 4: Most complex Python code
- **Multi-agent research assistant:** https://github.com/Rodix69/multi-agent-research-assistant
- [One line: what it does, and the hardest part, e.g. how the agents coordinate or share state.]

### Task 5: Most complex database code
- **Telecom churn MLOps pipeline (Phase 2):** https://github.com/Rodix69/production-grade-MLOps-framework
- Most relevant file: [`1_load_to_postgres.py`](https://github.com/Rodix69/production-grade-MLOps-framework/blob/phase-02-data-engineering/phase_02_data_engineering/src/1_load_to_postgres.py)
- PostgreSQL schema with a primary key and five indexes, idempotent chunked bulk loading of about 243K rows, and a paginated, filterable FastAPI layer over the database.
- This is my most substantial database work to date. I have not yet built multi-table, heavily transactional systems.

## Assignment 2

The written answers are in `LLM_Chatbots_and_Vector_Databases_Assignment.docx`:

1. Self-rating (LLM, Deep Learning, AI, ML)
2. Key architectural components of an LLM-based chatbot, with a high-level approach
3. Vector databases, including a hypothetical scenario (a university chatbot over about 10,000 PDFs), a comparison of options, and the choice of Qdrant with its trade-offs against PostgreSQL + pgvector

## Assumptions

- **Task 1:** I used Open Library (`https://openlibrary.org/search.json`) with the query "python" and a limit of 10 results.
- **Task 2:** The provided scores endpoint streams events instead of returning a JSON list, so the script reads the stream incrementally with a time and event limit. Scores slightly above 1.0 occasionally appear in the data and were kept as-is. The endpoint is a third-party service and may become unavailable.
- **Task 3:** I created a sample `users.csv` containing a duplicate email and an incomplete row to demonstrate the validation.
- **General:** Tasks use only `requests` and `matplotlib` beyond the Python standard library. Generated files (`books.db`, `users.db`, `scores.png`) are created in the working directory.
