import sqlite3
from contextlib import contextmanager

DATABASE = 'hotel.db'


def init_db():
    """Инициализация базы данных с таблицей комнат"""
    with get_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_id INTEGER UNIQUE NOT NULL,
                floor INTEGER NOT NULL,
                guest_num INTEGER NOT NULL,
                beds INTEGER NOT NULL,
                price INTEGER NOT NULL,
                booked INTEGER DEFAULT 0
            )
        ''')
        conn.commit()
        count = conn.execute('SELECT COUNT(*) FROM rooms').fetchone()[0]
        if count == 0:
            conn.execute('''
                INSERT INTO rooms (room_id, floor, guest_num, beds, price)
                VALUES (1, 2, 1, 1, 2000)
            ''')
            conn.execute('''
                INSERT INTO rooms (room_id, floor, guest_num, beds, price)
                VALUES (2, 1, 2, 1, 2500)
            ''')
            conn.commit()


@contextmanager
def get_connection():
    """Контекстный менеджер для работы с БД"""
    conn = sqlite3.connect(DATABASE)
    try:
        yield conn
    finally:
        conn.close()