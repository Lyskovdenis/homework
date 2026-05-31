import sqlite3
from pathlib import Path

from flask import Flask, render_template, redirect, url_for, g
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config["SECRET_KEY"] = "change_me_please"  # нужно для CSRF во Flask-WTF

# ----- Путь к БД -----

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "books.db"


# ----- Работа с БД -----

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
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


# ----- Форма WTForms -----

class BookForm(FlaskForm):
    book_title = StringField(
        "Book title",
        validators=[InputRequired(message="Title is required")],
    )
    author_name = StringField(
        "Author full name",
        validators=[InputRequired(message="Author is required")],
    )


# ----- Маршруты -----

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
    """Страница с формой добавления новой книги (с валидацией WTForms)."""
    init_db()
    form = BookForm()

    if form.validate_on_submit():
        title = form.book_title.data.strip()
        author = form.author_name.data.strip()

        insert_book(title, author)
        return redirect(url_for("get_books"))

    # если GET или валидация не прошла — снова показываем форму с ошибками
    return render_template("add_book.html", form=form)


if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(debug=True)