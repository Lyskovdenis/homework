PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS movie_direction;
DROP TABLE IF EXISTS oscar_awarded;
DROP TABLE IF EXISTS movie_cast;
DROP TABLE IF EXISTS director;
DROP TABLE IF EXISTS movie;
DROP TABLE IF EXISTS actors;

CREATE TABLE actors (
    act_id INTEGER PRIMARY KEY,
    act_first_name VARCHAR(50),
    act_last_name VARCHAR(50),
    act_gender VARCHAR(1)
);

CREATE TABLE movie (
    mov_id INTEGER PRIMARY KEY,
    mov_title VARCHAR(50)
);

CREATE TABLE director (
    dir_id INTEGER PRIMARY KEY,
    dir_first_name VARCHAR(50),
    dir_last_name VARCHAR(50)
);

CREATE TABLE movie_cast (
    act_id INTEGER,
    mov_id INTEGER,
    role VARCHAR(50),
    PRIMARY KEY (act_id, mov_id),
    FOREIGN KEY (act_id) REFERENCES actors(act_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (mov_id) REFERENCES movie(mov_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE oscar_awarded (
    award_id INTEGER PRIMARY KEY,
    mov_id INTEGER,
    FOREIGN KEY (mov_id) REFERENCES movie(mov_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE movie_direction (
    dir_id INTEGER,
    mov_id INTEGER,
    PRIMARY KEY (dir_id, mov_id),
    FOREIGN KEY (dir_id) REFERENCES director(dir_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (mov_id) REFERENCES movie(mov_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);