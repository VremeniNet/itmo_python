"""
Контроллер бизнес-логики для сущности Currency.
"""

from typing import List, Optional
from .databasecontroller import CurrencyRatesCRUD


class CurrencyController:
    """Контроллер CRUD для валют."""

    def __init__(self, db: CurrencyRatesCRUD):
        self._db = db

    def add_currency(
        self,
        num_code: str,
        char_code: str,
        name: str,
        value: float,
        nominal: int
    ) -> int:
        """Создаёт валюту и возвращает её ID."""
        return self._db._create(
            num_code,
            char_code,
            name,
            value,
            nominal
        )

    def list_currencies(self) -> List[dict]:
        """Возвращает список всех валют в словарях."""
        return self._db._read()

    def get_currency_by_char_code(self, char_code: str) -> Optional[dict]:
        """Возвращает валюту по букв. коду."""
        char_code = char_code.upper()
        for c in self._db._read():
            if c["char_code"].upper() == char_code:
                return c
        return None

    def update_value(self, char_code: str, new_value: float) -> None:
        """Обновляет курс валюты."""
        self._db._update({char_code: new_value})

    def delete_currency(self, currency_id: int) -> None:
        """Удаляет валюту по ID."""
        self._db._delete(currency_id)
