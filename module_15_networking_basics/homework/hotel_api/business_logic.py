from .database import get_connection
from .models import Room


def get_rooms_service():
    """Получить все комнаты из БД"""
    with get_connection() as conn:
        rows = conn.execute('''
            SELECT id, room_id, floor, guest_num, beds, price, booked
            FROM rooms
        ''').fetchall()
        return [Room.from_db_row(row) for row in rows]


def add_room_service(floor, guest_num, beds, price):
    """Добавить новую комнату в БД"""
    with get_connection() as conn:
        max_id = conn.execute('SELECT MAX(room_id) FROM rooms').fetchone()[0]
        new_room_id = max_id + 1 if max_id else 1

        conn.execute('''
            INSERT INTO rooms (room_id, floor, guest_num, beds, price)
            VALUES (?, ?, ?, ?, ?)
        ''', (new_room_id, floor, guest_num, beds, price))
        conn.commit()

        return Room(new_room_id, floor, guest_num, beds, price)


def booking_room_service(room_id):
    """Бронировать комнату по room_id"""
    with get_connection() as conn:
        row = conn.execute('''
            SELECT booked FROM rooms WHERE room_id = ?
        ''', (room_id,)).fetchone()

        if row is None:
            return False, 404

        if row[0] == 1:
            return False, 409

        conn.execute('''
            UPDATE rooms SET booked = 1 WHERE room_id = ?
        ''', (room_id,))
        conn.commit()

        return True, 200