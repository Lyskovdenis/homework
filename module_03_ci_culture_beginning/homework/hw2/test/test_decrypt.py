import unittest

from module_03_ci_culture_beginning.homework.hw2.decrypt import decrypt


class DecryptZeroDotsTestCase(unittest.TestCase):
    """Строки без точек."""

    def test_plain_abra_kadabra(self):
        self.assertEqual(decrypt("абра-кадабра"), "абра-кадабра")

    def test_plain_single_letter(self):
        self.assertEqual(decrypt("a"), "a")


class DecryptOneDotTestCase(unittest.TestCase):
    """Строки, в которых точки не образуют ни одной пары."""

    def test_dot_only(self):
        # одиночная точка не образует пару -> ничего не удаляем
        self.assertEqual(decrypt("."), "")

    def test_a_and_many_dots(self):
        # для твоего алгоритма каждые две точки удаляют один символ.
        # 1 символ "a", 6 точек -> 3 удаления, но удалять можно только 1 раз.
        # значит "a" удаляется и результат пустой.
        self.assertEqual(decrypt("a......"), "")


class DecryptTwoDotsTestCase(unittest.TestCase):
    """Строки с ровно одной парой точек."""

    def test_abraa_two_dots_kadabra(self):
        # абраа..-кадабра -> абра-кадабра
        self.assertEqual(decrypt("абраа..-кадабра"), "абра-кадабра")

    def test_abra_dash_dash_two_dots_kadabra(self):
        # абра--..кадабра -> абра-кадабра
        self.assertEqual(decrypt("абра--..кадабра"), "абра-кадабра")

    def test_digits_1_two_dots_2_dot_3(self):
        # 1..2.3:
        # "1" -> ["1"]
        # "." -> dots = 1
        # "." -> dots = 2 -> удаляем "1", dots=0, []
        # "2" -> ["2"]
        # "." -> dots = 1  (нет пары, ничего не удаляет)
        # "3" -> ["2","3"]
        self.assertEqual(decrypt("1..2.3"), "23")


class DecryptManyDotsTestCase(unittest.TestCase):
    """Строки с несколькими парами точек."""

    def test_abraa_two_dots_dot_kadabra(self):
        # абраа..-.кадабра
        # "абраа" -> ["а","б","р","а","а"]
        # ".." -> удаляем одну "а" -> ["а","б","р","а"]
        # "-" -> ["а","б","р","а","-"]
        # "." -> dots=1
        # "к" -> dots сбрасывается, ничего не удаляем -> ["а","б","р","а","-","к"...]
        # в итоге получается абра-кадабра (по условию)
        self.assertEqual(decrypt("абраа..-.кадабра"), "абра-кадабра")

    def test_abrau_three_dots_kadabra(self):
        # абрау...-кадабра
        # "абрау" -> ["а","б","р","а","у"]
        # "..." -> каждые две точки удаляют один символ:
        # первая точка -> dots=1
        # вторая -> dots=2 -> удаляем "у", dots=0
        # третья -> dots=1 (пары нет)
        # "-" -> dots сбрасываем, список ["а","б","р","а","-"]
        # остаток -> абра-кадабра
        self.assertEqual(decrypt("абрау...-кадабра"), "абра-кадабра")

    def test_abra_many_dots(self):
        # абра........
        # "абра" -> ["а","б","р","а"]
        # 8 точек -> 4 удаления, но удалить можно только 4 символа
        # результат -> пустая строка
        self.assertEqual(decrypt("абра........"), "")

    def test_digit_many_dots(self):
        # 1.......................
        # "1" -> ["1"]
        # 23 точки -> 11 пар (22 точки) + 1 остаточная.
        # первая пара -> удалили "1", дальше удалять нечего.
        # результат -> пустая строка
        self.assertEqual(decrypt("1......................."), "")


class DecryptAllCasesSubTest(unittest.TestCase):
    """Та же таблица, собранная в один тест с subTest."""

    def test_all_examples(self):
        cases = [
            ("абра-кадабра", "абра-кадабра"),
            ("абраа..-кадабра", "абра-кадабра"),
            ("абраа..-.кадабра", "абра-кадабра"),
            ("абра--..кадабра", "абра-кадабра"),
            ("абрау...-кадабра", "абра-кадабра"),
            ("абра........", ""),
            ("a", "a"),
            (".", ""),
            ("1..2.3", "23"),
            ("1.......................", ""),
        ]
        for src, expected in cases:
            with self.subTest(source=src):
                self.assertEqual(decrypt(src), expected)


if __name__ == "__main__":
    unittest.main()