from datetime import datetime, timedelta

from flask import Flask, jsonify, request, abort

from models import SessionLocal, Book, Student, ReceivingBook

app = Flask(__name__)


def get_session():
    return SessionLocal()


@app.get("/books")
def get_books():
    session = get_session()
    try:
        books = session.query(Book).all()
        result = [
            {
                "id": b.id,
                "name": b.name,
                "count": b.count,
                "release_date": b.release_date.isoformat(),
                "author_id": b.author_id,
            }
            for b in books
        ]
        return jsonify(result)
    finally:
        session.close()


@app.get("/debtors")
def get_debtors():
    session = get_session()
    try:
        # Книги, которые не сданы и у студента больше 14 дней
        fourteen_days_ago = datetime.now() - timedelta(days=14)

        q = (
            session.query(ReceivingBook, Student, Book)
            .join(Student, ReceivingBook.student_id == Student.id)
            .join(Book, ReceivingBook.book_id == Book.id)
            .filter(
                ReceivingBook.date_of_return.is_(None),
                ReceivingBook.date_of_issue < fourteen_days_ago,
            )
        )

        result = []
        for rb, st, bk in q.all():
            result.append(
                {
                    "student_id": st.id,
                    "student_name": f"{st.name} {st.surname}",
                    "book_id": bk.id,
                    "book_name": bk.name,
                    "date_of_issue": rb.date_of_issue.isoformat(),
                    "days_with_book": rb.count_date_with_book,
                }
            )
        return jsonify(result)
    finally:
        session.close()


@app.post("/issue")
def issue_book():
    data = request.get_json() or {}
    book_id = data.get("book_id")
    student_id = data.get("student_id")

    if not book_id or not student_id:
        abort(400, "book_id and student_id are required")

    session = get_session()
    try:
        book = session.query(Book).get(book_id)
        student = session.query(Student).get(student_id)
        if not book or not student:
            abort(404, "Book or student not found")

        # можно проверить наличие свободных экземпляров, если учитывать count
        rb = ReceivingBook(
            book_id=book_id,
            student_id=student_id,
            date_of_issue=datetime.now(),
            date_of_return=None,
        )
        session.add(rb)
        session.commit()
        return jsonify({"status": "ok", "receiving_id": rb.id}), 201
    finally:
        session.close()


@app.post("/return")
def return_book():
    data = request.get_json() or {}
    book_id = data.get("book_id")
    student_id = data.get("student_id")

    if not book_id or not student_id:
        abort(400, "book_id and student_id are required")

    session = get_session()
    try:
        rb = (
            session.query(ReceivingBook)
            .filter(
                ReceivingBook.book_id == book_id,
                ReceivingBook.student_id == student_id,
                ReceivingBook.date_of_return.is_(None),
            )
            .first()
        )
        if not rb:
            abort(404, "Active receiving record not found for this book and student")

        rb.date_of_return = datetime.now()
        session.commit()
        return jsonify({"status": "ok", "receiving_id": rb.id})
    finally:
        session.close()


@app.get("/books/search")
def search_books():
    query = request.args.get("query", "").strip()
    if not query:
        abort(400, "query parameter is required")

    session = get_session()
    try:
        books = (
            session.query(Book)
            .filter(Book.name.ilike(f"%{query}%"))
            .all()
        )
        result = [
            {"id": b.id, "name": b.name, "count": b.count,
             "release_date": b.release_date.isoformat(), "author_id": b.author_id}
            for b in books
        ]
        return jsonify(result)
    finally:
        session.close()


if __name__ == "__main__":
    app.run(debug=True)