import sqlite3
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for, g

app = Flask(__name__)

# Путь к файлу БД
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "books.db"


# ---------- Работа с БД ----------

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row  # чтобы получать dict-подобные строки
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Создаёт таблицу books, если её ещё нет."""
    db = get_db()
    cur = db.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL
        )
        """
    )
    db.commit()


def insert_book(title: str, author: str) -> None:
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO books (title, author) VALUES (?, ?)",
        (title, author),
    )
    db.commit()


def get_all_books():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT id, title, author FROM books ORDER BY id DESC")
    return cur.fetchall()


# ---------- Маршруты ----------

@app.route("/")
def index():
    return redirect(url_for("get_books"))


@app.route("/books")
def get_books():
    """Страница со списком книг."""
    init_db()
    books = get_all_books()
    return render_template("books.html", books=books)


@app.route("/books/form", methods=["GET", "POST"])
def get_books_form():
    """Страница с формой добавления новой книги."""
    init_db()

    if request.method == "POST":
        title = request.form.get("book_title", "").strip()
        author = request.form.get("author_name", "").strip()

        if not title or not author:
            error = "Both title and author are required"
            return render_template("add_book.html", error=error)

        insert_book(title, author)
        return redirect(url_for("get_books"))

    # GET-запрос — просто показать форму
    return render_template("add_book.html")


if __name__ == "__main__":
    # При первом запуске убедимся, что БД и таблица есть
    with app.app_context():
        init_db()
    app.run(debug=True)