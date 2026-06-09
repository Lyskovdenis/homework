from marshmallow import Schema, fields, validates, ValidationError, post_load
from models import Author, Book, get_book_by_title, get_author_by_id, add_author, get_books_by_author_id


class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    middle_name = fields.Str(allow_none=True)

    books = fields.Nested('BookShortSchema', many=True, dump_only=True)

    @post_load
    def create_author(self, data: dict, **kwargs) -> Author:
        return Author(**data)


class BookShortSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)


class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author_id = fields.Int(required=False, allow_none=True)
    author = fields.Nested(AuthorSchema, required=False)

    @validates('title')
    def validate_title(self, title: str, **kwargs) -> None:
        existing = get_book_by_title(title)
        if existing is not None:
            raise ValidationError(
                f'Book with title "{title}" already exists, '
                f'please use a different title.'
            )

    @validates('author_id')
    def validate_author_id(self, author_id: int | None, **kwargs) -> None:
        if author_id is None:
            return
        if get_author_by_id(author_id) is None:
            raise ValidationError(
                f'Author with id "{author_id}" does not exist.'
            )

    @post_load
    def create_book(self, data: dict, **kwargs) -> Book:
        author_obj = data.pop('author', None)
        if author_obj:
            # author_obj уже Author, т.к. AuthorSchema в своём post_load делает Author(**data)
            new_author = add_author(author_obj)
            data['author_id'] = new_author.id
        return Book(**data)