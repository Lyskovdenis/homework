import unittest
import datetime

from module_03_ci_culture_beginning.homework.hw4.person import Person


class PersonTestCase(unittest.TestCase):
    """Тесты для класса Person: проверяем все методы."""

    @classmethod
    def setUpClass(cls):
        """Подготавливаем базовые данные для тестов."""
        cls.current_year = datetime.datetime.now().year

    def setUp(self):
        """Создаём новый объект Person перед каждым тестом."""
        self.person = Person(name="Иван", year_of_birth=self.current_year - 30)

    # --- get_age ---

    def test_get_age_returns_correct_age(self):
        """get_age: возраст должен совпадать с разницей между текущим годом и годом рождения."""
        expected_age = self.current_year - self.person.yob
        self.assertEqual(self.person.get_age(), expected_age)

    # --- get_name / set_name ---

    def test_get_name_initial(self):
        """get_name: возвращает имя, переданное в конструктор."""
        self.assertEqual(self.person.get_name(), "Иван")

    def test_set_name_changes_name(self):
        """set_name: должен изменять имя объекта."""
        self.person.set_name("Пётр")
        self.assertEqual(self.person.get_name(), "Пётр")

    # --- set_address / get_address ---

    def test_get_address_initial_is_empty_string(self):
        """get_address: по умолчанию адрес пустая строка."""
        self.assertEqual(self.person.get_address(), "")

    def test_set_address_changes_address(self):
        """set_address: должен изменять адрес объекта."""
        self.person.set_address("Москва, ул. Пушкина, д. 1")
        self.assertEqual(self.person.get_address(), "Москва, ул. Пушкина, д. 1")

    # --- is_homeless ---

    def test_is_homeless_true_when_address_empty(self):
        """is_homeless: True, если адрес пустая строка (по умолчанию)."""
        self.assertTrue(self.person.is_homeless())

    def test_is_homeless_true_when_address_none(self):
        """is_homeless: True, если адрес None."""
        p = Person(name="Анна", year_of_birth=2000, address=None)
        self.assertTrue(p.is_homeless())

    def test_is_homeless_false_when_address_set(self):
        """is_homeless: False, если адрес задан непустой строкой."""
        self.person.set_address("СПб, Невский проспект, д. 10")
        self.assertFalse(self.person.is_homeless())


if __name__ == "__main__":
    unittest.main()
