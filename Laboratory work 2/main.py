from typing import Iterable, List, Literal, Optional, Tuple

GuessMethod = Literal["linear", "binary"]


def guess_linear(target: int, pool: Iterable[int]) -> Optional[Tuple[int, int]]:
    """Угадать число медленным перебором (инкрементом).

    Перебирает значения по возрастанию от минимального до максимального
    в предоставленном пуле (даже если список был неотсортирован).
    На каждой проверке увеличивает счётчик попыток на 1.

    Args:
        target: Загаданное число, которое нужно угадать.
        pool: Коллекция допустимых значений (без повторов).

    Returns:
        (угаданное_число, число_попыток) или None, если target отсутствует
        в пуле либо число не удалось найти (что маловероятно при корректных данных).
    """
    s = set(pool)
    if target not in s:
        return None

    attempts = 0
    current = min(s)
    finish = max(s)

    while current <= finish:
        attempts += 1
        if current == target:
            return current, attempts
        current += 1

    return None


def guess_binary(target: int, pool: Iterable[int]) -> Optional[Tuple[int, int]]:
    """Угадать число бинарным поиском.

    Для корректной работы бинарного поиска данные сортируются (копия),
    так как исходный список по условию может быть неотсортирован.
    На каждом сравнении с элементом середины увеличивается счётчик попыток на 1.

    Args:
        target: Загаданное число, которое нужно угадать.
        pool: Коллекция допустимых значений (без повторов).

    Returns:
        (угаданное_число, число_попыток) или None, если target отсутствует
        в пуле либо не найден бинарным поиском.
    """
    s = set(pool)
    if target not in s:
        return None

    arr = sorted(s)
    left, right = 0, len(arr) - 1
    attempts = 0

    while left <= right:
        mid = (left + right) // 2
        attempts += 1
        if arr[mid] == target:
            return arr[mid], attempts
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return None


def guess_number(
    target: int,
    pool: Iterable[int],
    method: GuessMethod = "linear",
) -> Optional[Tuple[int, int]]:
    """Унифицированная функция угадывания числа.

    Принимает загаданное число, список (или другой итерируемый объект)
    допустимых значений и метод угадывания. Возвращает кортеж из найденного
    числа и количества попыток/сравнений.

    По условию входной список может быть неотсортирован и не содержит повторов;
    для бинарного поиска внутри функции создаётся отсортированная копия.

    Args:
        target: Загаданное число.
        pool: Список/итерируемый объект допустимых значений.
        method: "linear" (медленный перебор) или "binary" (бинарный поиск).

    Returns:
        (угаданное_число, число_попыток) или None, если метод некорректен
        либо число отсутствует в пуле/не найдено.
    """
    if method == "linear":
        return guess_linear(target, pool)
    if method == "binary":
        return guess_binary(target, pool)
    return None


def build_pool(start: int, end: int) -> List[int]:
    """Сформировать пул значений как список целых в диапазоне [start, end].

    Args:
        start: Начало диапазона (включительно).
        end: Конец диапазона (включительно). Может быть меньше start — порядок нормализуется.

    Returns:
        Список int: [min(start,end), ..., max(start,end)].
    """
    lo, hi = sorted((start, end))
    return list(range(lo, hi + 1))


def read_from_keyboard() -> Tuple[int, List[int], GuessMethod]:
    """Вспомогательная функция для ввода параметров с клавиатуры.

    Последовательно запрашивает:
      - начало диапазона,
      - конец диапазона,
      - загаданное число,
      - метод угадывания ("linear" или "binary").

    Выполняет базовую валидацию и возвращает готовые параметры для guess_number().

    Returns:
        Кортеж (target, pool, method).
    """
    while True:
        try:
            start = int(input("Введите начало диапазона (целое число): ").strip())
            end = int(input("Введите конец диапазона (целое число): ").strip())
            pool = build_pool(start, end)

            target = int(input("Введите загаданное число: ").strip())
            if target not in pool:
                lo, hi = min(pool), max(pool)
                print(f"Число вне диапазона [{lo}; {hi}]. Попробуйте снова.\n")
                continue

            method_str = input(
                'Выберите метод ("linear" или "binary"): '
            ).strip().lower()
            if method_str not in ("linear", "binary"):
                print('Метод должен быть "linear" или "binary". Попробуйте снова.\n')
                continue

            return target, pool, method_str
        except ValueError:
            print("Ожидалось целое число. Попробуйте снова.\n")


if __name__ == "__main__":
    tgt, numbers, how = read_from_keyboard()
    result = guess_number(tgt, numbers, how)
    print(result)
    if result is None:
        print("\nНе удалось угадать число (проверьте корректность входных данных).")
    else:
        value, attempts = result
        print(f"\nУгадано число: {value}")
        print(f"Количество попыток: {attempts}")
