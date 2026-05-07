import unittest
from block_errors import BlockErrors


class BlockErrorsTestCase(unittest.TestCase):
    def test_zero_division_suppressed(self):
        # Ошибка из списка должна подавляться
        try:
            with BlockErrors({ZeroDivisionError}):
                1 / 0
        except Exception as e:
            self.fail(f"Exception was not suppressed: {e!r}")

    def test_unexpected_error_not_suppressed(self):
        # Ошибка не из списка должна быть прокинута
        with self.assertRaises(ZeroDivisionError):
            with BlockErrors({TypeError}):
                1 / 0

    def test_nested_blocks(self):
        # Пример с вложенными блоками
        outer_err_types = {TypeError}
        inner_err_types = {ZeroDivisionError}

        # ZeroDivisionError подавляется внутренним блоком
        with BlockErrors(inner_err_types):
            1 / 0

        # TypeError подавляется внешним
        try:
            with BlockErrors(outer_err_types):
                1 / "0"  # TypeError
        except TypeError:
            self.fail("Outer BlockErrors should have suppressed TypeError")

    def test_exception_base_suppresses_all(self):
        # Exception должен подавлять всё, что от него наследуется
        try:
            with BlockErrors({Exception}):
                1 / "0"
        except Exception as e:
            self.fail(f"Exception was not suppressed: {e!r}")


if __name__ == '__main__':
    unittest.main()