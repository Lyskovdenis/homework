"""
Для каждого поля и валидатора в эндпоинте /registration напишите юнит-тест,
который проверит корректность работы валидатора. Таким образом, нужно проверить, что существуют наборы данных,
которые проходят валидацию, и такие, которые валидацию не проходят.
"""

import unittest

from module_04_flask.homework.hw1_3.hw1_registration import app


class RegistrationFormValidatorsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        cls.client = app.test_client()

    # -------- email --------

    def test_email_valid(self):
        """email: корректный адрес проходит валидацию."""
        resp = self.client.post(
            "/registration",
            data={
                "email": "user@example.com",
                "phone": "1234567890",
                "name": "Denis",
                "address": "Minsk",
                "index": "220000",
                "comment": "",
            },
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Successfully registered user", resp.get_data(as_text=True))

    def test_email_invalid_format(self):
        """email: некорректный формат не проходит валидацию."""
        resp = self.client.post(
            "/registration",
            data={
                "email": "notemail",
                "phone": "1234567890",
                "name": "Denis",
                "address": "Minsk",
                "index": "220000",
                "comment": "",
            },
        )
        self.assertEqual(resp.status_code, 400)
        text = resp.get_data(as_text=True)
        self.assertIn("email", text)  # есть ошибка по полю email

    def test_email_required(self):
        """email: пустое значение не проходит (обязательное поле)."""
        resp = self.client.post(
            "/registration",
            data={
                "email": "",
                "phone": "1234567890",
                "name": "Denis",
                "address": "Minsk",
                "index": "220000",
                "comment": "",
            },
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn("email", resp.get_data(as_text=True))

    # -------- phone --------

    def test_phone_valid(self):
        """phone: 10‑значное положительное число проходит валидацию."""
        resp = self.client.post(
            "/registration",
            data={
                "email": "user@example.com",
                "phone": "1234567890",  # 10 цифр
                "name": "Denis",
                "address": "Minsk",
                "index": "220000",
                "comment": "",
            },
        )
        self.assertEqual(resp.status_code, 200)

    def test_phone_too_short(self):
        """phone: слишком короткое число не проходит (NumberLength)."""
        resp = self.client.post(
            "/registration",
            data={
                "email": "user@example.com",
                "phone": "12345",  # 5 цифр
                "name": "Denis",
                "address": "Minsk",
                "index": "220000",
                "comment": "",
            },
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn("phone", resp.get_data(as_text=True))

    def test_phone_negative(self):
        """phone: отрицательное число не проходит (NumberRange min=0)."""
        resp = self.client.post(
            "/registration",
            data={
                "email": "user@example.com",
                "phone": "-1234567890",
                "name": "Denis",
                "address": "Minsk",
                "index": "220000",
                "comment": "",
            },
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn("phone", resp.get_data(as_text=True))

    def test_phone_required(self):
        """phone: пустое значение не проходит (обязательное поле)."""
        resp = self.client.post(
            "/registration",
            data={
                "email": "user@example.com",
                "phone": "",
                "name": "Denis",
                "address": "Minsk",
                "index": "220000",
                "comment": "",
            },
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn("phone", resp.get_data(as_text=True))

    # -------- name --------

    def test_name_valid(self):
        """name: непустое имя проходит валидацию."""
        resp = self.client.post(
            "/registration",
            data={
                "email": "user@example.com",
                "phone": "1234567890",
                "name": "Denis",
                "address": "Minsk",
                "index": "220000",
                "comment": "",
            },
        )
        self.assertEqual(resp.status_code, 200)

    def test_name_required(self):
        """name: пустое значение не проходит (обязательное поле)."""
        resp = self.client.post(
            "/registration",
            data={
                "email": "user@example.com",
                "phone": "1234567890",
                "name": "",
                "address": "Minsk",
                "index": "220000",
                "comment": "",
            },
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn("name", resp.get_data(as_text=True))

    # -------- address --------

    def test_address_valid(self):
        """address: непустой адрес проходит валидацию."""
        resp = self.client.post(
            "/registration",
            data={
                "email": "user@example.com",
                "phone": "1234567890",
                "name": "Denis",
                "address": "Minsk",
                "index": "220000",
                "comment": "",
            },
        )
        self.assertEqual(resp.status_code, 200)

    def test_address_required(self):
        """address: пустое значение не проходит (обязательное поле)."""
        resp = self.client.post(
            "/registration",
            data={
                "email": "user@example.com",
                "phone": "1234567890",
                "name": "Denis",
                "address": "",
                "index": "220000",
                "comment": "",
            },
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn("address", resp.get_data(as_text=True))

    # -------- index --------

    def test_index_valid(self):
        """index: числовое значение проходит валидацию."""
        resp = self.client.post(
            "/registration",
            data={
                "email": "user@example.com",
                "phone": "1234567890",
                "name": "Denis",
                "address": "Minsk",
                "index": "220000",
                "comment": "",
            },
        )
        self.assertEqual(resp.status_code, 200)

    def test_index_required(self):
        """index: пустое значение не проходит (обязательное поле)."""
        resp = self.client.post(
            "/registration",
            data={
                "email": "user@example.com",
                "phone": "1234567890",
                "name": "Denis",
                "address": "Minsk",
                "index": "",
                "comment": "",
            },
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn("index", resp.get_data(as_text=True))

    def test_index_must_be_number(self):
        """index: нечисловое значение не проходит (IntegerField)."""
        resp = self.client.post(
            "/registration",
            data={
                "email": "user@example.com",
                "phone": "1234567890",
                "name": "Denis",
                "address": "Minsk",
                "index": "abcde",
                "comment": "",
            },
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn("index", resp.get_data(as_text=True))

    # -------- comment --------

    def test_comment_optional_empty_is_ok(self):
        """comment: пустое значение допускается (Optional)."""
        resp = self.client.post(
            "/registration",
            data={
                "email": "user@example.com",
                "phone": "1234567890",
                "name": "Denis",
                "address": "Minsk",
                "index": "220000",
                "comment": "",
            },
        )
        self.assertEqual(resp.status_code, 200)

    def test_comment_optional_nonempty_is_ok(self):
        """comment: произвольный текст тоже проходит (поле опционально)."""
        resp = self.client.post(
            "/registration",
            data={
                "email": "user@example.com",
                "phone": "1234567890",
                "name": "Denis",
                "address": "Minsk",
                "index": "220000",
                "comment": "Some comment",
            },
        )
        self.assertEqual(resp.status_code, 200)


if __name__ == "__main__":
    unittest.main()