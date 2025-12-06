# Лабораторная работа №7  
## Логирование, декораторы, исключения, работа с внешним API
## Желанов Даниил, P4150

---

## 1. Исходный код декоратора с параметрами.

```python

import logging
import functools
import sys
from datetime import datetime


def logger(func=None, *, handle=sys.stdout):
    """
    Декоратор для логирования вызовов функций.

    Args:
        func: Декорируемая функция.
        handle: Поток для вывода логов или экземпляр logging.Logger.
    """

    def resolve_writers():
        """
        В зависимости от типа handle возвращает две функции:
        info_writer(message) и error_writer(message).
        """
        if isinstance(handle, logging.Logger):

            def info_writer(message: str) -> None:
                handle.info(message)

            def error_writer(message: str) -> None:
                handle.error(message)
        else:
            def write(prefix: str, text: str) -> None:
                handle.write(f"{prefix}{text}\n")

            def info_writer(message: str) -> None:
                write("INFO: ", message)

            def error_writer(message: str) -> None:
                write("ERROR: ", message)

        return info_writer, error_writer

    info_log, error_log = resolve_writers()

    def timestamp() -> str:
        """Вернуть текущий момент времени в виде строки."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def format_call(fn, args, kwargs) -> str:
        """
        Сформировать представление вызова функции
        """
        parts = []
        if args:
            parts.extend(repr(arg) for arg in args)
        if kwargs:
            parts.extend(f"{name}={repr(value)}" for name, value in kwargs.items())
        joined = ", ".join(parts)
        return f"{fn.__name__}({joined})"

    def decorator(target):
        @functools.wraps(target)
        def wrapped(*args, **kwargs):
            call_repr = format_call(target, args, kwargs)
            info_log(f"[{timestamp()}] Вызов функции {call_repr}")

            try:
                result = target(*args, **kwargs)
            except Exception as exc:
                error_log(
                    f"[{timestamp()}] "
                    f"В функции {target.__name__} произошло исключение "
                    f"{type(exc).__name__}: {exc}"
                )
                raise
            else:
                info_log(
                    f"[{timestamp()}] "
                    f"Функция {target.__name__} успешно завершена. "
                    f"Результат: {repr(result)}"
                )
                return result

        return wrapped

    if func is not None and callable(func):
        return decorator(func)

    return decorator

```

## 2. Исходный код ```get_currencies```(без логирования).

```python
import requests


def get_currencies(
    currency_codes: list,
    url: str = "https://www.cbr-xml-daily.ru/daily_json.js",
) -> dict:
    """
    Получает курсы валют с API ЦБ РФ.

    Args:
        currency_codes: Список кодов валют, курсы которых нужно вернуть.
        url: Адрес API ЦБ РФ.

    Returns:
        Словарь с курсами валют в формате {"USD": 93.25, "EUR": 101.7}.

    Raises:
        ConnectionError: Если API недоступен или произошла сетевая ошибка.
        ValueError: Если ответ не удалось разобрать как корректный JSON.
        KeyError: Если нет ключа "Valute" или запрошенный код валюты отсутствует.
        TypeError: Если курс валюты имеет неверный тип.
    """
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise ConnectionError(f"API недоступно: {exc}") from exc

    try:
        payload = response.json()
    except ValueError as exc:
        raise ValueError(f"Некорректный JSON от API: {exc}") from exc

    try:
        valute_block = payload["Valute"]
    except KeyError as exc:
        raise KeyError("В JSON-ответе отсутствует ключ 'Valute'") from exc

    if not isinstance(valute_block, dict):
        raise TypeError("Поле 'Valute' имеет неверный формат")

    rates: dict[str, float] = {}

    for code in currency_codes:
        try:
            currency_data = valute_block[code]
        except KeyError as exc:
            raise KeyError(f"Код валюты '{code}' отсутствует в данных API") from exc

        if not isinstance(currency_data, dict):
            raise TypeError(f"Описание валюты '{code}' имеет неверный формат")

        if "Value" not in currency_data:
            raise KeyError(f"В данных по валюте '{code}' нет поля 'Value'")

        value = currency_data["Value"]

        if not isinstance(value, (int, float)):
            raise TypeError(
                f"Курс валюты '{code}' имеет неверный тип: {type(value).__name__}"
            )

        rates[code] = float(value)

    return rates
```

## 3. Демонстрационный пример (квадратное уравнение).

```python
import math
import sys
import logging

from logger import logger


# логгер для квадратного уравнения
quadratic_logger = logging.getLogger("quadratic")
quadratic_logger.setLevel(logging.INFO)

_stream_handler = logging.StreamHandler(sys.stdout)
_stream_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
quadratic_logger.addHandler(_stream_handler)


@logger(handle=quadratic_logger)
def solve_quadratic(a: float, b: float, c: float) -> tuple[float, ...] | None:
    """
    Решает квадратное уравнение вида ax^2 + bx + c = 0.

    Args:
        a: Коэффициент при x^2.
        b: Коэффициент при x.
        c: Свободный член.

    Returns:
        Кортеж корней (один или два) либо None, если действительных корней нет.

    Логирование:
        - INFO    — информация о найденных корнях;
        - WARNING — отрицательный дискриминант (нет действительных корней);
        - ERROR   — некорректные данные (например, a = "abc");
        - CRITICAL — полностью невозможная ситуация (a и b равны нулю).
    """
    # 1. Проверяем корректность типов
    for name, value in (("a", a), ("b", b), ("c", c)):
        if not isinstance(value, (int, float)):
            quadratic_logger.error(
                "Коэффициент %s имеет недопустимый тип: %r", name, value
            )
            raise TypeError(f"Коэффициент {name} должен быть числом")

    # 2. Обрабатываем особые случаи с a и b
    if a == 0 and b == 0:
        quadratic_logger.critical(
            "Невозможная ситуация: a и b одновременно равны нулю"
        )
        raise ValueError("Коэффициенты a и b не могут быть одновременно равны нулю")

    if a == 0:
        # линейное уравнение bx + c = 0
        x = -c / b
        quadratic_logger.info("Линейное уравнение, единственный корень: %s", x)
        return (x,)

    # 3. Классический случай: считаем дискриминант
    d = b ** 2 - 4 * a * c
    quadratic_logger.info("Дискриминант D = %s", d)

    if d < 0:
        quadratic_logger.warning(
            "Дискриминант отрицательный (D < 0) — действительных корней нет"
        )
        return None

    if d == 0:
        x = -b / (2 * a)
        quadratic_logger.info("Один действительный корень: x = %s", x)
        return (x,)

    # d > 0 — два действительных корня
    sqrt_d = math.sqrt(d)
    x1 = (-b + sqrt_d) / (2 * a)
    x2 = (-b - sqrt_d) / (2 * a)
    quadratic_logger.info("Два действительных корня: x1 = %s, x2 = %s", x1, x2)
    return x1, x2


if __name__ == "__main__":
    # INFO: два корня
    solve_quadratic(1, -3, 2)

    # WARNING: дискриминант < 0
    solve_quadratic(1, 0, 1)

    # ERROR: некорректные данные (a = "abc")
    try:
        solve_quadratic("abc", 1, 1)
    except TypeError:
        pass

    # CRITICAL: невозможная ситуация a = b = 0
    try:
        solve_quadratic(0, 0, 5)
    except ValueError:
        pass

```

## 4. Фрагменты логов

### 4.1 ```demo_quadratic.py```:

<img width="1478" height="412" alt="image" src="https://github.com/user-attachments/assets/640d46a0-4ae5-4570-bd80-876bf786fe5f" />


### 4.3 ```main.py```:

<img width="988" height="157" alt="image" src="https://github.com/user-attachments/assets/c2889eee-e15c-4b58-85dd-1677d532a7b0" />


### 4.4 ```currencies.log```:

<img width="1166" height="83" alt="image" src="https://github.com/user-attachments/assets/b694cef8-f1e1-46fc-84b4-c82dcb504619" />

## 5. Тесты

### 5.1 Тесты функции get_currencies (test_currencies.py)

```python
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

```

**Результат выполнения тестов функции:**

<img width="411" height="205" alt="image" src="https://github.com/user-attachments/assets/6e41a041-75a9-4e2a-b936-aef929bfcfe2" />


### 5.2 Тесты декоратора (test_logger.py)

```python
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

```

**Результат выполнения тестов декоратора:**

<img width="397" height="173" alt="image" src="https://github.com/user-attachments/assets/b34193f7-da97-4cce-b25b-1a4604bd850d" />


### 5.3 Работа с StringIO

```python
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
```
