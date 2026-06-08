import sqlite3
from dataclasses import dataclass
from typing import Optional, Union, List

INITIAL_AUTHORS = [
    {'first_name': 'Swaroop', 'last_name': 'C. H.', 'middle_name': None},
    {'first_name': 'Herman', 'last_name': 'Melville', 'middle_name': None},
    {'first_name': 'Leo', 'last_name': 'Tolstoy', 'middle_name': None},
]

INITIAL_BOOKS = [
    {'title': 'A Byte of Python', 'author_index': 0},
    {'title': 'Moby-Dick; or, The Whale', 'author_index': 1},
    {'title': 'War and Peace', 'author_index': 2},
]

DATABASE_NAME = 'table_books.db'
BOOKS_TABLE_NAME = 'books'
AUTHORS_TABLE_NAME = 'authors'


@dataclass
class Author:
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    id: Optional[int] = None

    def __getitem__(self, item: str) -> Union[int, str, None]:
        return getattr(self, item)


@dataclass
class Book:
    title: str
    author_id: int
    id: Optional[int] = None

    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)


def init_db() -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name=?;
            """,
            (BOOKS_TABLE_NAME,),
        )
        exists = cursor.fetchone()
        if exists:
            return  # схема уже есть, ничего не делаем

        cursor.executescript(
            f"""
            CREATE TABLE `{AUTHORS_TABLE_NAME}`(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name  TEXT NOT NULL,
                last_name   TEXT NOT NULL,
                middle_name TEXT
            );

            CREATE TABLE `{BOOKS_TABLE_NAME}`(
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                title     TEXT NOT NULL,
                author_id INTEGER NOT NULL,
                FOREIGN KEY (author_id) REFERENCES `{AUTHORS_TABLE_NAME}`(id)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            );
            """
        )

        cursor.executemany(
            f"""
            INSERT INTO `{AUTHORS_TABLE_NAME}` (first_name, last_name, middle_name)
            VALUES (?, ?, ?)
            """,
            [
                (a['first_name'], a['last_name'], a['middle_name'])
                for a in INITIAL_AUTHORS
            ],
        )

        cursor.execute(f"SELECT id FROM `{AUTHORS_TABLE_NAME}` ORDER BY id")
        author_ids = [row[0] for row in cursor.fetchall()]

        cursor.executemany(
            f"""
            INSERT INTO `{BOOKS_TABLE_NAME}` (title, author_id)
            VALUES (?, ?)
            """,
            [
                (b['title'], author_ids[b['author_index']])
                for b in INITIAL_BOOKS
            ],
        )

        conn.commit()


def _get_author_obj_from_row(row: tuple) -> Author:
    return Author(
        id=row[0],
        first_name=row[1],
        last_name=row[2],
        middle_name=row[3],
    )


def _get_book_obj_from_row(row: tuple) -> Book:
    return Book(id=row[0], title=row[1], author_id=row[2])


# -------- AUTHORS --------

def add_author(author: Author) -> Author:
    with sqlite3.connect(DATABASE_NAME) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO `{AUTHORS_TABLE_NAME}` (first_name, last_name, middle_name)
            VALUES (?, ?, ?)
            """,
            (author.first_name, author.last_name, author.middle_name),
        )
        author.id = cursor.lastrowid
        conn.commit()
        return author


def get_author_by_id(author_id: int) -> Optional[Author]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT * FROM `{AUTHORS_TABLE_NAME}` WHERE id = ?",
            (author_id,),
        )
        row = cursor.fetchone()
        if row:
            return _get_author_obj_from_row(row)
        return None


def delete_author_by_id(author_id: int) -> None:
    """Удаляет автора и все его книги благодаря ON DELETE CASCADE."""
    with sqlite3.connect(DATABASE_NAME) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()
        cursor.execute(
            f"""
            DELETE FROM `{AUTHORS_TABLE_NAME}`
            WHERE id = ?
            """,
            (author_id,),
        )
        conn.commit()


def get_books_by_author_id(author_id: int) -> List[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}` WHERE author_id = ?
            """,
            (author_id,),
        )
        rows = cursor.fetchall()
        return [_get_book_obj_from_row(row) for row in rows]


# -------- BOOKS --------

def get_all_books() -> list[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM `{BOOKS_TABLE_NAME}`")
        rows = cursor.fetchall()
        return [_get_book_obj_from_row(row) for row in rows]


def add_book(book: Book) -> Book:
    with sqlite3.connect(DATABASE_NAME) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO `{BOOKS_TABLE_NAME}` (title, author_id)
            VALUES (?, ?)
            """,
            (book.title, book.author_id),
        )
        book.id = cursor.lastrowid
        conn.commit()
        return book


def get_book_by_id(book_id: int) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}` WHERE id = ?
            """,
            (book_id,)
        )
        row = cursor.fetchone()
        if row:
            return _get_book_obj_from_row(row)
        return None


def update_book_by_id(book: Book) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()
        cursor.execute(
            f"""
            UPDATE `{BOOKS_TABLE_NAME}`
            SET title = ?, author_id = ?
            WHERE id = ?
            """,
            (book.title, book.author_id, book.id),
        )
        conn.commit()


def delete_book_by_id(book_id: int) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            DELETE FROM `{BOOKS_TABLE_NAME}`
            WHERE id = ?
            """,
            (book_id,)
        )
        conn.commit()


def get_book_by_title(book_title: str) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}` WHERE title = ?
            """,
            (book_title,)
        )
        row = cursor.fetchone()
        if row:
            return _get_book_obj_from_row(row)
        return None