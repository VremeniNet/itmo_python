import unittest
import io

from logger import logger


class TestLoggerDecorator(unittest.TestCase):
    """Тестирование поведения параметризуемого декоратора logger."""

    def setUp(self):
        """Создаём поток StringIO, чтобы перехватывать вывод декоратора."""
        self.buffer = io.StringIO()

        @logger(handle=self.buffer)
        def sample(x, y=1):
            return x + y

        @logger(handle=self.buffer)
        def faulty(x):
            raise ValueError("boom")

        self.sample = sample
        self.faulty = faulty

    def test_logging_success(self):
        """Проверяет логи при успешном выполнении функции."""
        result = self.sample(3, y=4)
        logs = self.buffer.getvalue()

        # результат функции возвращается корректно
        self.assertEqual(result, 7)

        # должен быть лог о старте (INFO)
        self.assertIn("INFO", logs)
        self.assertIn("sample(3, y=4)", logs)

        # должен быть лог об успешном окончании
        self.assertIn("успешно завершена", logs)
        self.assertIn("7", logs)

    def test_logging_error(self):
        """Проверяет логи при возникновении ошибки и проброс исключения."""
        with self.assertRaises(ValueError):
            self.faulty(10)

        logs = self.buffer.getvalue()

        self.assertIn("ERROR", logs)
        self.assertIn("ValueError", logs)
        self.assertIn("boom", logs)



if __name__ == "__main__":
    unittest.main()
