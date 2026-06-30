from datetime import datetime
from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, Float,
    Date, DateTime, ForeignKey
)
from sqlalchemy.orm import (
    declarative_base, relationship, sessionmaker
)
from sqlalchemy.ext.associationproxy import association_proxy

Base = declarative_base()

# путь к БД — как в прошлой задаче, поправь под свой проект
engine = create_engine("sqlite:///../materials/library.db", echo=False)
SessionLocal = sessionmaker(bind=engine)


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)

    # One-to-many: автор -> книги
    books = relationship(
        "Book",
        back_populates="author",
        cascade="all, delete-orphan",
        lazy="selectin",      # жадная подгрузка коллекции
    )


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)

    author = relationship(
        "Author",
        back_populates="books",
        lazy="joined",        # жадная подгрузка автора через JOIN
    )

    # One-to-many: книга -> выдачи
    receivings = relationship(
        "ReceivingBook",
        back_populates="book",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)

    # One-to-many: студент -> выдачи
    receivings = relationship(
        "ReceivingBook",
        back_populates="student",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    # MANY-TO-MANY через association_proxy:
    # студент.books — список книг, которые он брал
    books = association_proxy("receivings", "book")


class ReceivingBook(Base):
    __tablename__ = "receiving_books"

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    date_of_issue = Column(DateTime, nullable=False)
    date_of_return = Column(DateTime)

    book = relationship(
        "Book",
        back_populates="receivings",
        lazy="joined",      # жадная загрузка книги
    )
    student = relationship(
        "Student",
        back_populates="receivings",
        lazy="joined",      # жадная загрузка студента
    )