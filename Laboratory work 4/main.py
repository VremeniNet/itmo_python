from __future__ import annotations

import sys
import statistics
import timeit
from typing import Iterable, List, Dict, Callable, Optional

import matplotlib.pyplot as plt


# ВСПОМОГАТЕЛЬНОЕ
def _is_valid_n(n: object) -> bool:
    """Проверить, что `n` — целое неотрицательное.

    Args:
        n: Произвольное значение.

    Returns:
        bool: True — если `n` является int и `n >= 0`, иначе False.
    """
    return isinstance(n, int) and n >= 0


# ФУНКЦИИ
def fact_recursive(n: int) -> Optional[int]:
    """Вычислить факториал рекурсивно (без кеширования).

    Прямая рекурсия: n! = n × (n-1)!; базовый случай — 0! и 1! равны 1.

    Args:
        n (int): Неотрицательное целое число.

    Returns:
        int | None: Значение `n!` либо `None`, если `n` некорректен.
    """
    if not _is_valid_n(n):
        return None

    def _rec(k: int) -> int:
        if k < 2:
            return 1
        return k * _rec(k - 1)

    return _rec(n)


def fact_iterative(n: int) -> Optional[int]:
    """Вычислить факториал итеративно (через цикл).

    Линейный проход по диапазону [2; n] с накоплением произведения.

    Args:
        n (int): Неотрицательное целое число.

    Returns:
        int | None: Значение `n!` либо `None`, если `n` некорректен.
    """
    if not _is_valid_n(n):
        return None
    result = 1
    for k in range(2, n + 1):
        result *= k
    return result


def benchmark_single(func: Callable[[int], Optional[int]], n: int, repeat: int = 10) -> float:
    """Измерить «чистое» время одного вызова функции.

    Запускает `timeit` с `number=1` (ровно один вызов) и повторяет измерение
    несколько раз; в качестве оценки возвращает медиану.

    Args:
        func: Тестируемая функция.
        n (int): Аргумент для вызова.
        repeat (int): Число повторов. По умолчанию 10.

    Returns:
        float: Медианное время одного вызова в секундах.
    """
    timer = timeit.Timer(lambda: func(n))
    samples = timer.repeat(repeat=repeat, number=1)
    return statistics.median(samples)


def benchmark_series(ns: Iterable[int], repeats: int = 5) -> Dict[str, List[float]]:
    """Провести серию измерений на фиксированном наборе `n`.

    Для каждого `n` выполняется несколько измерений обеих реализаций
    и берётся медиана. Один и тот же набор `n` используется для обеих функций.

    Args:
        ns: Набор входных значений `n` (фиксированный список).
        repeats: Повторов на каждую точку. По умолчанию 5.

    Returns:
        dict: Согласованные списки:
            - 'n' — значения n;
            - 'iterative_ms' — времена итеративной версии (мс, медиана);
            - 'recursive_ms' — времена рекурсивной версии (мс, медиана).
    """
    ns = list(ns)
    iter_times_ms: List[float] = []
    rec_times_ms: List[float] = []

    for n in ns:
        t_iter = timeit.repeat(lambda: fact_iterative(n), repeat=repeats, number=1)
        iter_times_ms.append(1000.0 * statistics.median(t_iter))

        t_rec = timeit.repeat(lambda: fact_recursive(n), repeat=repeats, number=1)
        rec_times_ms.append(1000.0 * statistics.median(t_rec))

    return {"n": ns, "iterative_ms": iter_times_ms, "recursive_ms": rec_times_ms}


def plot_results(series: Dict[str, List[float]], out_path: str = "factorial_benchmark.png") -> str:
    """Построить график времени выполнения и сохранить в PNG.

    Args:
        series: Результат `benchmark_series`.
        out_path: Путь для сохранения PNG. По умолчанию 'factorial_benchmark.png'.

    Returns:
        str: Путь к сохранённому файлу.
    """
    plt.figure()
    plt.plot(series["n"], series["iterative_ms"], marker="o", label="Итеративная")
    plt.plot(series["n"], series["recursive_ms"], marker="o", label="Рекурсивная")
    plt.xlabel("n (размер входа)")
    plt.ylabel("Время, мс (медиана)")
    plt.title("Факториал: время — итеративная vs рекурсивная (без raise)")
    plt.legend()
    plt.grid(True, which="both", linestyle="--", alpha=0.4)
    plt.savefig(out_path, dpi=160, bbox_inches="tight")
    return out_path


# MAIN
def main() -> None:
    """Запустить бенчмарки, вывести таблицу и построить график.

    Формирует фиксированный список входов `n`, проводит серию измерений,
    печатает таблицу, выполняет «чистый» бенчмарк одного вызова
    и сохраняет график в PNG-файл.
    """
    # Запас от лимита рекурсии, чтобы избежать RecursionError.
    buffer = 50
    max_safe = sys.getrecursionlimit() - buffer

    # Фиксированный набор n для честного сравнения.
    n_values = [10, 110, 210, 310, 410, 510, 610, 710]
    n_values = [n for n in n_values if n <= max_safe]

    # Серийный бенчмарк (медиана по повторам).
    series = benchmark_series(n_values, repeats=7)

    # Таблица результатов.
    print("Результаты (медиана по повторам):")
    print(f"{'n':>6} | {'итеративная, мс':>16} | {'рекурсивная, мс':>16}")
    print("-" * 47)
    for n, ti, tr in zip(series["n"], series["iterative_ms"], series["recursive_ms"]):
        print(f"{n:6d} | {ti:16.3f} | {tr:16.3f}")

    # «Чистый» бенчмарк одного вызова.
    n0 = 310 if 310 in series["n"] else series["n"][len(series["n"]) // 2]
    single_iter_ms = 1000.0 * benchmark_single(fact_iterative, n0, repeat=15)
    single_rec_ms = 1000.0 * benchmark_single(fact_recursive, n0, repeat=15)
    ratio = (single_rec_ms / single_iter_ms) if single_iter_ms > 0 else float("inf")

    print("\nЧистый бенчмарк одного вызова (мс, медиана):")
    print(f"n = {n0}: итеративная = {single_iter_ms:.3f} мс, рекурсивная = {single_rec_ms:.3f} мс")
    print(f"Отношение (рекурсивная / итеративная) = {ratio:.2f}×")

    # График.
    out_path = plot_results(series)
    print(f"\nГрафик сохранён: {out_path}")


if __name__ == "__main__":
    main()
