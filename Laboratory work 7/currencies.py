import requests
import sys
import logging

from logger import logger

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

# Обернуть функцию декоратором
@logger(handle=sys.stdout)
def get_currencies_stdout(codes: list, url: str = "https://www.cbr-xml-daily.ru/daily_json.js") -> dict:
    """Обёртка над get_currencies с логированием в стандартный вывод."""
    return get_currencies(codes, url=url)

# Самостоятельная часть
file_log = logging.getLogger("currency_file")
file_log.setLevel(logging.INFO)

file_handler = logging.FileHandler("currencies.log", encoding="utf-8")
file_handler.setLevel(logging.INFO)

file_log.addHandler(file_handler)

@logger(handle=file_log)
def get_currencies_file(codes: list, url: str = "https://www.cbr-xml-daily.ru/daily_json.js") -> dict:
    """Обёртка над get_currencies с логированием в файл."""
    return get_currencies(codes, url=url)