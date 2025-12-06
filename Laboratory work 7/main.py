from logger import logger
from currencies import get_currencies


@logger()
def fetch_and_print_rates(codes: list) -> None:
    """
    Запрашивает курсы указанных валют и выводит их в консоль.

    Args:
        codes: Список кодов валют, например ["USD", "EUR"].
    """
    rates = get_currencies(codes)
    print("Текущие курсы валют:")
    for code, value in rates.items():
        print(f"  {code}: {value}")


if __name__ == "__main__":
    try:
        fetch_and_print_rates(["USD", "EUR"])
    except Exception as err:
        print(f"Во время получения курсов произошла ошибка: {err}")