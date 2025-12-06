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
