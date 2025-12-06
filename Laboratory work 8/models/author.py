"""
Модели предметной области: автор приложения.

Содержит класс Author с полями:
- name  — имя автора;
- group — учебная группа.

Класс предоставляет геттеры и сеттеры с базовой проверкой корректности данных.
"""


class Author:
    """Информация об авторе приложения."""

    def __init__(self, name: str, group: str) -> None:
        self.name = name
        self.group = group

    @property
    def name(self) -> str:
        """Имя автора."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Имя автора должно быть строкой")
        value = value.strip()
        if not value:
            raise ValueError("Имя автора не может быть пустым")
        self._name = value

    @property
    def group(self) -> str:
        """Учебная группа автора."""
        return self._group

    @group.setter
    def group(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Группа должна быть строкой")
        value = value.strip()
        if not value:
            raise ValueError("Группа не может быть пустой")
        self._group = value

    def __repr__(self) -> str:
        return f"Author(name={self.name!r}, group={self.group!r})"

    def __str__(self) -> str:
        return f"{self.name} ({self.group})"
