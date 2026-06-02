class Room:
    """Модель комнаты"""

    def __init__(self, room_id, floor, guest_num, beds, price, booked=False):
        self.room_id = room_id
        self.floor = floor
        self.guest_num = guest_num
        self.beds = beds
        self.price = price
        self.booked = booked

    @classmethod
    def from_db_row(cls, row):
        """Создать объект Room из строки БД"""
        return cls(
            room_id=row[1],
            floor=row[2],
            guest_num=row[3],
            beds=row[4],
            price=row[5],
            booked=bool(row[6])
        )