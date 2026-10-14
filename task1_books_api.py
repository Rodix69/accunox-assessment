import sqlite3
import requests

API_URL = "https://openlibrary.org/search.json"

def fetch_books(query="python", limit=10):
    resp = requests.get(API_URL, params={"q": query, "limit": limit}, timeout=10)
    resp.raise_for_status()                      # fail loudly on 4xx/5xx
    books = []
    for doc in resp.json().get("docs", []):
        books.append((
            doc.get("title", "Unknown"),
            ", ".join(doc.get("author_name", ["Unknown"])),
            doc.get("first_publish_year"),       # may be None
        ))
    return books

def save_books(books, db_path="books.db"):
    with sqlite3.connect(db_path) as conn:       # commits on success, rolls back on error
        conn.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT,
                year INTEGER,
                UNIQUE(title, author)
            )""")
        conn.executemany(
            "INSERT OR IGNORE INTO books (title, author, year) VALUES (?, ?, ?)",
            books,
        )

def show_books(db_path="books.db"):
    with sqlite3.connect(db_path) as conn:
        for title, author, year in conn.execute(
            "SELECT title, author, year FROM books ORDER BY year"
        ):
            print(f"{year or 'n/a'} | {title} | {author}")

if __name__ == "__main__":
    save_books(fetch_books())
    show_books()