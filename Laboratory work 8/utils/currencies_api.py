"""
Работа с API курсов валют ЦБ РФ.

Содержит функцию get_currencies, которая:
- запрашивает JSON по заданному URL;
- извлекает словарь Valute;
- возвращает словарь курсов вида {"USD": 93.25, "EUR": 101.7};
- выбрасывает исключения при ошибках сети или данных.
"""

import requests


def get_currencies(
    currency_codes: list,
    url: str = "https://www.cbr-xml-daily.ru/daily_json.js",
) -> dict:
    """
    Получает курсы валют с API ЦБ РФ.

    Args:
        currency_codes: список кодов валют (например, ["USD", "EUR"])
        url: URL API ЦБ РФ

    Returns:
        Словарь с курсами валют:
        {"USD": 93.25, "EUR": 101.7}

    Raises:
        ConnectionError: если API недоступен
        ValueError: если получен некорректный JSON
        KeyError: если нет ключа "Valute" или отсутствует валюта в данных
        TypeError: если курс валюты имеет неверный тип
    """
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        raise ConnectionError(f"API недоступен: {exc}") from exc

    try:
        data = response.json()
    except ValueError as exc:
        raise ValueError(f"Некорректный JSON: {exc}") from exc

    if "Valute" not in data:
        raise KeyError("Нет ключа 'Valute' в ответе API")

    valute_data = data["Valute"]
    result: dict[str, float] = {}

    for code in currency_codes:
        if code not in valute_data:
            raise KeyError(f"Валюта {code} отсутствует в данных")

        info = valute_data[code]

        if "Value" not in info:
            raise KeyError(f"Нет ключа 'Value' для валюты {code}")

        rate = info["Value"]

        if not isinstance(rate, (int, float)):
            raise TypeError(
                f"Курс валюты {code} имеет неверный тип: {type(rate).__name__}"
            )

        result[code] = float(rate)

    return result
