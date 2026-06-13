-- таблица книг в библиотеке books
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    count INT DEFAULT 1,
    release_date DATE NOT NULL,
    author_id INT NOT NULL
);

-- таблица авторов authors
CREATE TABLE IF NOT EXISTS authors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    surname TEXT NOT NULL
);

-- таблица читателей students
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL,
    average_score FLOAT NOT NULL,
    scholarship BOOLEAN NOT NULL
);

-- таблица выдачи книг студентам receiving_books
CREATE TABLE IF NOT EXISTS receiving_books (
    id INTEGER PRIMARY KEY,
    book_id INT NOT NULL,
    student_id INT NOT NULL,
    date_of_issue DATETIME NOT NULL,
    date_of_return DATETIME
);