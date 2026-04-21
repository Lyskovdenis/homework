import datetime


class Person:
    def __init__(self, name: str, year_of_birth: int, address: str = ""):
        self.name = name
        self.yob = year_of_birth
        self.address = address

    def get_age(self) -> int:
        """Возвращает возраст на текущий год."""
        now = datetime.datetime.now()
        return now.year - self.yob

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    def set_address(self, address: str) -> None:
        self.address = address

    def get_address(self) -> str:
        return self.address

    def is_homeless(self) -> bool:
        """
        Возвращает True, если адрес не задан (None или пустая строка),
        False в противном случае.
        """
        return not self.address