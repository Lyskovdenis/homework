import unittest
from remote_execution import app


class RemoteExecutionTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_timeout_less_than_execution_time(self):
        # Код спит дольше тайм-аута → должен вернуться 408
        code = "import time; time.sleep(2); print('done')"
        resp = self.client.post(
            "/run_code",
            data={"code": code, "timeout": 1},
        )
        self.assertEqual(resp.status_code, 408)
        text = resp.get_data(as_text=True)
        self.assertIn("Execution did not finish in 1 seconds", text)

    def test_invalid_form_data(self):
        # Пустой код и некорректный тайм-аут → 400 и ошибки валидации
        resp = self.client.post(
            "/run_code",
            data={"code": "", "timeout": 100},
        )
        self.assertEqual(resp.status_code, 400)
        data = resp.get_json()
        self.assertIn("code", data["errors"])
        self.assertIn("timeout", data["errors"])

    def test_unsafe_input_no_shell_injection(self):
        bad_code = 'print("ok")"; import os; os.system("echo hacked")'
        resp = self.client.post(
            "/run_code",
            data={"code": bad_code, "timeout": 5},
        )
        self.assertEqual(resp.status_code, 200)
        text = resp.get_data(as_text=True)
        parts = text.split("Stderr:\n", 1)
        stdout_part = parts[0]  # "Stdout:\n<stdout>"

        self.assertNotIn("hacked", stdout_part)


if __name__ == "__main__":
    unittest.main()
