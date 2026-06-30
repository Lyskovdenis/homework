from datetime import datetime, date
from calendar import monthrange

from flask import Flask, jsonify, request, abort
from sqlalchemy import func

from models import SessionLocal, Author, Book, Student, ReceivingBook

app = Flask(__name__)


def get_session():
    return SessionLocal()


@app.get("/authors/<int:author_id>/books_left")
def books_left_by_author(author_id: int):
    session = get_session()
    try:
        # всего экземпляров
        total_count = session.query(func.coalesce(func.sum(Book.count), 0)).filter(
            Book.author_id == author_id
        ).scalar()

        # текущих выдач (не возвращено)
        active_issues = (
            session.query(func.count(ReceivingBook.id))
            .join(Book, ReceivingBook.book_id == Book.id)
            .filter(
                Book.author_id == author_id,
                ReceivingBook.date_of_return.is_(None),
            )
            .scalar()
        )

        left = total_count - active_issues
        return jsonify({"author_id": author_id, "books_left": left})
    finally:
        session.close()


@app.get("/students/<int:student_id>/unread_books_same_authors")
def unread_books_same_authors(student_id: int):
    session = get_session()
    try:
        # авторы, кого студент уже читал
        read_author_ids_subq = (
            session.query(Book.author_id)
            .join(ReceivingBook, ReceivingBook.book_id == Book.id)
            .filter(ReceivingBook.student_id == student_id)
            .distinct()
            .subquery()
        )

        # книги этих авторов, которые студент НЕ брал
        unread_books = (
            session.query(Book)
            .filter(Book.author_id.in_(read_author_ids_subq))
            .filter(~Book.id.in_(
                session.query(ReceivingBook.book_id)
                .filter(ReceivingBook.student_id == student_id)
            ))
            .all()
        )

        result = [
            {
                "book_id": b.id,
                "book_name": b.name,
                "author_id": b.author_id,
                "author_name": f"{b.author.name} {b.author.surname}",
            }
            for b in unread_books
        ]
        return jsonify(result)
    finally:
        session.close()


@app.get("/stats/avg_books_this_month")
def avg_books_this_month():
    session = get_session()
    try:
        today = date.today()
        first_day = date(today.year, today.month, 1)
        last_day = date(today.year, today.month, monthrange(today.year, today.month)[1])

        # количество выдач по студентам в этом месяце
        per_student_counts = (
            session.query(
                ReceivingBook.student_id,
                func.count(ReceivingBook.id).label("cnt"),
            )
            .filter(
                ReceivingBook.date_of_issue >= first_day,
                ReceivingBook.date_of_issue <= last_day,
            )
            .group_by(ReceivingBook.student_id)
            .subquery()
        )

        avg_cnt = session.query(func.avg(per_student_counts.c.cnt)).scalar() or 0
        return jsonify({"avg_books_this_month": float(avg_cnt)})
    finally:
        session.close()


@app.get("/stats/most_popular_book_highscore")
def most_popular_book_highscore():
    session = get_session()
    try:
        q = (
            session.query(
                Book.id,
                Book.name,
                func.count(ReceivingBook.id).label("issue_count"),
            )
            .join(ReceivingBook, ReceivingBook.book_id == Book.id)
            .join(Student, ReceivingBook.student_id == Student.id)
            .filter(Student.average_score > 4.0)
            .group_by(Book.id, Book.name)
            .order_by(func.count(ReceivingBook.id).desc())
            .limit(1)
        )

        row = q.first()
        if not row:
            return jsonify({"most_popular_book": None})

        return jsonify(
            {
                "book_id": row.id,
                "book_name": row.name,
                "issue_count": row.issue_count,
            }
        )
    finally:
        session.close()


@app.get("/stats/top_readers_this_year")
def top_readers_this_year():
    session = get_session()
    try:
        year = datetime.now().year
        start = datetime(year, 1, 1)
        end = datetime(year, 12, 31, 23, 59, 59)

        q = (
            session.query(
                Student.id,
                Student.name,
                Student.surname,
                func.count(ReceivingBook.id).label("books_count"),
            )
            .join(ReceivingBook, ReceivingBook.student_id == Student.id)
            .filter(
                ReceivingBook.date_of_issue >= start,
                ReceivingBook.date_of_issue <= end,
            )
            .group_by(Student.id, Student.name, Student.surname)
            .order_by(func.count(ReceivingBook.id).desc())
            .limit(10)
        )

        result = [
            {
                "student_id": row.id,
                "student_name": f"{row.name} {row.surname}",
                "books_count": row.books_count,
            }
            for row in q.all()
        ]
        return jsonify(result)
    finally:
        session.close()


import csv
from io import TextIOWrapper

@app.post("/students/upload_csv")
def upload_students_csv():
    if "file" not in request.files:
        abort(400, "CSV file is required")

    file = request.files["file"]
    if file.filename == "":
        abort(400, "Empty filename")

    # Оборачиваем в TextIOWrapper, чтобы DictReader читал текст
    wrapper = TextIOWrapper(file.stream, encoding="utf-8")
    reader = csv.DictReader(wrapper, delimiter=";")

    # Подготовить список словарей для bulk_insert_mappings
    students_data = []
    for row in reader:
        # Приведение типов
        students_data.append(
            {
                "name": row["name"],
                "surname": row["surname"],
                "phone": row["phone"],
                "email": row["email"],
                "average_score": float(row["average_score"]),
                "scholarship": row["scholarship"].lower() in ("1", "true", "yes"),
            }
        )

    session = get_session()
    try:
        session.bulk_insert_mappings(Student, students_data)
        session.commit()
        return jsonify({"inserted": len(students_data)})
    finally:
        session.close()