import unittest
from typing import List


from main import (
    guess_number,
    guess_linear,
    guess_binary,
    build_pool,
)


class TestGuessNumber(unittest.TestCase):
    # --- helpers ------------------------------------------------------------
    def assertFound(self, res, target):
        """Проверка 'нашлось' с корректным числом и валидным счётчиком попыток."""
        self.assertIsNotNone(res, "Ожидался не-None результат")
        value, attempts = res
        self.assertEqual(value, target)
        self.assertIsInstance(attempts, int)
        self.assertGreater(attempts, 0)

    # 1. Таргет попадает
    def test_target_present_linear(self):
        pool = build_pool(1, 10)
        target = 7
        res = guess_number(target, pool, method="linear")
        self.assertFound(res, target)

        self.assertEqual(res[1], target)

    def test_target_present_binary(self):
        pool = build_pool(1, 1024)
        target = 777
        res = guess_number(target, pool, method="binary")
        self.assertFound(res, target)

    # 2. Таргет не попадает
    def test_target_absent_linear(self):
        pool = build_pool(10, 20)
        res = guess_number(25, pool, method="linear")
        self.assertIsNone(res)

    def test_target_absent_binary(self):
        pool = build_pool(10, 20)
        res = guess_number(9, pool, method="binary")
        self.assertIsNone(res)

    # 3. Диапазон пустой (передаём пустой список как пул)
    def test_empty_pool(self):
        pool: List[int] = []
        self.assertIsNone(guess_number(1, pool, method="linear"))
        self.assertIsNone(guess_number(1, pool, method="binary"))

    # 4. Диапазон из 1 числа
    def test_singleton_pool(self):
        pool = [5]
        self.assertEqual(guess_linear(5, pool), (5, 1))
        found = guess_binary(5, pool)
        self.assertEqual(found, (5, 1))

    # 5. Input порядок границ обратный

    def test_reversed_range(self):
        pool = build_pool(20, 10)  # должно стать [10..20]
        self.assertFound(guess_number(12, pool, "linear"), 12)
        self.assertFound(guess_number(19, pool, "binary"), 19)

    # 6. Input — float / string, которые можно преобразовать в int
    # a) float
    def test_convertible_float_target(self):
        pool = build_pool(1, 10)
        res_lin = guess_number(5.0, pool, "linear")
        res_bin = guess_number(5.0, pool, "binary")
        self.assertFound(res_lin, 5)
        self.assertFound(res_bin, 5)

    # b) string "6"
    def test_convertible_string_target_not_auto_casted(self):
        pool = build_pool(1, 10)
        self.assertIsNone(guess_number("6", pool, "linear"))

    # 7. Input — float / string, которые нельзя преобразовать в int
    def test_non_convertible_target(self):
        pool = build_pool(1, 10)
        self.assertIsNone(guess_number("abc", pool, "linear"))
        self.assertIsNone(guess_number("abc", pool, "binary"))

    # 8. Диапазон от отрицательных до положительных
    def test_negative_to_positive_range(self):
        pool = build_pool(-5, 5)
        self.assertFound(guess_number(-2, pool, "linear"), -2)
        self.assertFound(guess_number(3, pool, "binary"), 3)


    def test_unsorted_sparse_pool(self):
        pool = [10, 4, 7, 1, 3, 8]  # неотсортирован и не непрерывен
        self.assertFound(guess_number(7, pool, "linear"), 7)
        self.assertFound(guess_number(1, pool, "binary"), 1)


    def test_invalid_method(self):
        pool = build_pool(1, 5)
        res = guess_number(3, pool, method="something")
        self.assertIsNone(res)


if __name__ == "__main__":
    unittest.main()
