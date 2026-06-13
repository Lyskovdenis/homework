from datetime import datetime, date
from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean,
    Float, Date, DateTime
)
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()
engine = create_engine("sqlite:///../materials/library.db", echo=False)
SessionLocal = sessionmaker(bind=engine)


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    author_id = Column(Integer, nullable=False)


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)

    # 3.1. Студенты, имеющие общежитие (будем трактовать scholarship как признак льгот/общежития)
    @classmethod
    def with_scholarship(cls, session):
        """Список студентов, у которых scholarship = True."""
        return session.query(cls).filter(cls.scholarship.is_(True)).all()

    # 3.2. Студенты с средним баллом выше порога
    @classmethod
    def with_score_above(cls, session, threshold: float):
        """Студенты, у которых average_score > threshold."""
        return session.query(cls).filter(cls.average_score > threshold).all()


class ReceivingBook(Base):
    __tablename__ = "receiving_books"

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, nullable=False)
    student_id = Column(Integer, nullable=False)
    date_of_issue = Column(DateTime, nullable=False)
    date_of_return = Column(DateTime)

    # 2. hybrid_property: сколько дней книга у студента
    @hybrid_property
    def count_date_with_book(self) -> int:
        """Количество дней, сколько книга у студента.
        Если не сдал — считаем от date_of_issue до текущего времени.
        """
        end = self.date_of_return or datetime.now()
        return (end.date() - self.date_of_issue.date()).days

    @count_date_with_book.expression
    def count_date_with_book(cls):
        """SQL‑эквивалент для использования в фильтрах/ORDER BY."""
        # julianday('now') - julianday(date_of_issue)
        from sqlalchemy import func
        return func.cast(
            func.julianday(func.coalesce(cls.date_of_return, func.current_timestamp())) -
            func.julianday(cls.date_of_issue),
            Integer
        )


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)