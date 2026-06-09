from flask import Flask, request
from flask_restful import Api, Resource
from marshmallow import ValidationError

from models import (
    init_db,
    get_all_books,
    add_book,
    get_book_by_id,
    update_book_by_id,
    delete_book_by_id,
    get_author_by_id,
    add_author,
    delete_author_by_id,
    get_books_by_author_id,
)
from schemas import BookSchema, AuthorSchema

app = Flask(__name__)
api = Api(app)


class BookList(Resource):
    def get(self):
        schema = BookSchema()
        return schema.dump(get_all_books(), many=True), 200

    def post(self):
        data = request.get_json()
        schema = BookSchema()
        try:
            book = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        book = add_book(book)
        return schema.dump(book), 201


class BookDetail(Resource):
    # твои GET/PUT/DELETE/PATCH как уже сделано
    ...


class AuthorList(Resource):
    def post(self):
        """
        POST /api/authors — создание автора.
        Body:
        {
          "name": "Leo Tolstoy",
          "country": "Russia"
        }
        """
        data = request.get_json()
        schema = AuthorSchema()
        try:
            author = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        author = add_author(author)
        # для корректного вывода книг нужно подставить пустой список
        author.books = []
        return schema.dump(author), 201


class AuthorDetail(Resource):
    def get(self, author_id: int):
        """
        GET /api/authors/<id> — автор + все его книги.
        """
        author = get_author_by_id(author_id)
        if author is None:
            return {"message": "Author not found"}, 404

        # подтянем книги автора
        books = get_books_by_author_id(author_id)
        # динамически прикрепим список книг к объекту
        author.books = books

        schema = AuthorSchema()
        return schema.dump(author), 200

    def delete(self, author_id: int):
        """
        DELETE /api/authors/<id> — удалить автора и все его книги.
        """
        author = get_author_by_id(author_id)
        if author is None:
            return {"message": "Author not found"}, 404

        delete_author_by_id(author_id)
        return {"message": "Author and his books deleted"}, 204


api.add_resource(BookList, '/api/books')
api.add_resource(BookDetail, '/api/books/<int:book_id>')
api.add_resource(AuthorList, '/api/authors')
api.add_resource(AuthorDetail, '/api/authors/<int:author_id>')


if __name__ == '__main__':
    init_db()
    app.run(debug=True)