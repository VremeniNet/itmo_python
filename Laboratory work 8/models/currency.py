"""
Модель валюты.

Класс Currency описывает валюту в системе:

- id        — уникальный идентификатор;
- num_code  — цифровой код (например, 840 для USD);
- char_code — символьный код (например, 'USD');
- name      — полное название валюты;
- value     — курс относительно рубля;
- nominal   — номинал (за сколько единиц валюты указан курс).
"""


class Currency:
    """Информация о валюте и её текущем курсе."""

    def __init__(
        self,
        currency_id: int,
        num_code: int,
        char_code: str,
        name: str,
        value: float,
        nominal: int = 1,
    ) -> None:
        self.id = currency_id
        self.num_code = num_code
        self.char_code = char_code
        self.name = name
        self.value = value
        self.nominal = nominal


    @property
    def id(self) -> int:
        """Уникальный идентификатор валюты."""
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Идентификатор валюты должен быть целым числом")
        if value <= 0:
            raise ValueError("Идентификатор валюты должен быть положительным")
        self._id = value


    @property
    def num_code(self) -> int:
        """Цифровой код валюты (ISO 4217)."""
        return self._num_code

    @num_code.setter
    def num_code(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Цифровой код валюты должен быть целым числом")
        if value <= 0:
            raise ValueError("Цифровой код валюты должен быть положительным")
        self._num_code = value


    @property
    def char_code(self) -> str:
        """Символьный код валюты (например, 'USD')."""
        return self._char_code

    @char_code.setter
    def char_code(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Символьный код валюты должен быть строкой")
        value = value.strip().upper()
        if not value:
            raise ValueError("Символьный код валюты не может быть пустым")
        if len(value) > 4:
            raise ValueError("Символьный код валюты слишком длинный")
        self._char_code = value


    @property
    def name(self) -> str:
        """Полное название валюты."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Название валюты должно быть строкой")
        value = value.strip()
        if not value:
            raise ValueError("Название валюты не может быть пустым")
        self._name = value


    @property
    def value(self) -> float:
        """Курс валюты относительно рубля."""
        return self._value

    @value.setter
    def value(self, rate: float) -> None:
        if not isinstance(rate, (int, float)):
            raise TypeError("Курс валюты должен быть числом")
        if rate < 0:
            raise ValueError("Курс валюты должен быть положительным")
        self._value = float(rate)


    @property
    def nominal(self) -> int:
        """Номинал (за сколько единиц валюты указан курс)."""
        return self._nominal

    @nominal.setter
    def nominal(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Номинал должен быть целым числом")
        if value < 0:
            raise ValueError("Номинал должен быть положительным")
        self._nominal = value


    def __repr__(self) -> str:
        return (
            "Currency(id={id!r}, num_code={num!r}, char_code={char!r}, "
            "name={name!r}, value={val!r}, nominal={nom!r})"
        ).format(
            id=self.id,
            num=self.num_code,
            char=self.char_code,
            name=self.name,
            val=self.value,
            nom=self.nominal,
        )

    def __str__(self) -> str:
        return f"{self.char_code} ({self.name}): {self.value} за {self.nominal}"
