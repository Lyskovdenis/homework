import unittest

from freezegun import freeze_time
from module_03_ci_culture_beginning.homework.hw1.hello_word_with_day import app


class HelloWorldWeekdayTestCase(unittest.TestCase):
    def setUp(self) -> None:
        # создаём тестовый клиент Flask
        self.client = app.test_client()

    @freeze_time("2024-04-01")  # понедельник
    def test_monday_greeting(self):
        resp = self.client.get("/hello-world/Denis")
        text = resp.data.decode("utf-8")
        assert "Хорошего понедельника" in text

    @freeze_time("2024-04-02")  # вторник
    def test_tuesday_greeting(self):
        resp = self.client.get("/hello-world/Denis")
        text = resp.data.decode("utf-8")
        assert "Хорошего вторника" in text

    @freeze_time("2024-04-03")  # среда
    def test_wednesday_greeting(self):
        resp = self.client.get("/hello-world/Denis")
        text = resp.data.decode("utf-8")
        assert "Хорошей среды" in text

    @freeze_time("2024-04-04")  # четверг
    def test_thursday_greeting(self):
        resp = self.client.get("/hello-world/Denis")
        text = resp.data.decode("utf-8")
        assert "Хорошего четверга" in text

    @freeze_time("2024-04-05")  # пятница
    def test_friday_greeting(self):
        resp = self.client.get("/hello-world/Denis")
        text = resp.data.decode("utf-8")
        assert "Хорошей пятницы" in text

    @freeze_time("2024-04-06")  # суббота
    def test_saturday_greeting(self):
        resp = self.client.get("/hello-world/Denis")
        text = resp.data.decode("utf-8")
        assert "Хорошей субботы" in text

    @freeze_time("2024-04-07")  # воскресенье
    def test_sunday_greeting(self):
        resp = self.client.get("/hello-world/Denis")
        text = resp.data.decode("utf-8")
        assert "Хорошего воскресенья" in text


class HelloWorldUsernameCollisionTestCase(unittest.TestCase):
    """Проверяем случай, когда username уже содержит пожелание."""

    @freeze_time("2024-04-03")  # среда
    def test_username_is_already_greeting(self):
        """
        Если в качестве имени передать 'Хорошей среды',
        а день недели — не среда, можно легко промахнуться.
        Здесь мы фризим среду, чтобы убедиться, что:
        - в ответе есть настоящее пожелание для среды
        - и что username вставлен именно как имя.
        """
        name = "Хорошей среды"
        resp = app.test_client().get(f"/hello-world/{name}")
        text = resp.data.decode("utf-8")

        # username должен подставиться как есть
        assert "Привет, Хорошей среды." in text
        # а пожелание — именно зафиксированное по дню недели
        assert text.strip().endswith("Хорошей среды!")


if __name__ == "__main__":
    unittest.main()
