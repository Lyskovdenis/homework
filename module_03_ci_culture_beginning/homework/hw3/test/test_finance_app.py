import unittest

from module_03_ci_culture_beginning.homework.hw3.finance_app import app, storage


class FinanceAppTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # общий клиент для всех тестов
        cls.client = app.test_client()

    def setUp(self):
        # перед каждым тестом очищаем и заполняем storage базовым состоянием
        storage.clear()
        # базовые данные:
        # 2024-01-01: +100
        # 2024-01-02: +200
        # 2025-12-31: +50
        storage.update({
            2024: {
                1: {
                    1: 100,
                    2: 200,
                    'total': 300,
                },
                'total': 300,
            },
            2025: {
                12: {
                    31: 50,
                    'total': 50,
                },
                'total': 50,
            },
        })

    # --- Тесты для /add/ ---

    def test_add_valid_date_updates_storage(self):
        # добавляем 70 к 2024-01-03
        resp = self.client.get("/add/20240103/70")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Успешно добавлено", resp.data.decode("utf-8"))

        # проверяем, что данные в storage обновились корректно
        self.assertEqual(storage[2024][1][3], 70)
        self.assertEqual(storage[2024][1]['total'], 300 + 70)
        self.assertEqual(storage[2024]['total'], 300 + 70)

    def test_add_valid_date_existing_day(self):
        # 2024-01-01 уже есть со значением 100, добавляем ещё 50
        resp = self.client.get("/add/20240101/50")
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(storage[2024][1][1], 150)
        self.assertEqual(storage[2024][1]['total'], 300 + 50)
        self.assertEqual(storage[2024]['total'], 300 + 50)

    def test_add_invalid_date_raises_value_error(self):
        # дата не в формате YYYYMMDD: слишком короткая строка, парсинг int(date[4:6]) падает
        with self.assertRaises(ValueError):
            # важно: вызываем саму view-функцию add, а не клиент, чтобы увидеть исключение
            from module_03_ci_culture_beginning.homework.hw3.finance_app import add
            add("202401", 100)

    def test_add_invalid_date_client_sees_500(self):
        # через HTTP Flask перехватывает исключение и отдаёт 500
        resp = self.client.get("/add/202401/100")
        self.assertEqual(resp.status_code, 500)

    # --- Тесты для /calculate/<year> ---

    def test_calculate_year_existing_year(self):
        resp = self.client.get("/calculate/2024")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data.decode("utf-8"), "300")

    def test_calculate_year_other_year(self):
        resp = self.client.get("/calculate/2025")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data.decode("utf-8"), "50")

    def test_calculate_year_when_storage_empty(self):
        storage.clear()
        resp = self.client.get("/calculate/2024")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data.decode("utf-8"), "0")

    # --- Тесты для /calculate/<year>/<month> ---

    def test_calculate_month_existing_month(self):
        resp = self.client.get("/calculate/2024/1")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data.decode("utf-8"), "300")

    def test_calculate_month_other_month(self):
        resp = self.client.get("/calculate/2025/12")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data.decode("utf-8"), "50")

    def test_calculate_month_when_no_data_for_month(self):
        resp = self.client.get("/calculate/2024/2")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data.decode("utf-8"), "0")

    def test_calculate_month_when_storage_empty(self):
        storage.clear()
        resp = self.client.get("/calculate/2024/1")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data.decode("utf-8"), "0")


if __name__ == "__main__":
    unittest.main()