import unittest

from currencies import get_currencies

MAX_R_VALUE = 1000.0


class TestGetCurrencies(unittest.TestCase):
    def test_currency_usd_real_rate(self):
        """
        Проверяет, что для реальной валюты USD возвращается
        неотрицательное число разумного размера.
        """
        codes = ["USD"]
        data = get_currencies(codes)

        self.assertIn("USD", data)
        self.assertIsInstance(data["USD"], float)
        self.assertGreaterEqual(data["USD"], 0)
        self.assertLessEqual(data["USD"], MAX_R_VALUE)

    def test_nonexistent_code_raises_key_error(self):
        """
        Для несуществующего кода валюты должна выбрасываться ошибка KeyError.
        """
        with self.assertRaises(KeyError):
            get_currencies(["XYZ"])

    def test_connection_error_wrong_url(self):
        """
        При некорректном URL или недоступности API должен быть ConnectionError.
        """
        with self.assertRaises(ConnectionError):
            get_currencies(["USD"], url="https://")

    def test_invalid_json_raises_value_error(self):
        """
        Если по URL возвращается не JSON, должна выбрасываться ошибка ValueError.
        """
        with self.assertRaises(ValueError):
            get_currencies(["USD"], url="https://www.example.com")


if __name__ == "__main__":
    unittest.main()
