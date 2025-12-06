"""
Модель пользователя.

Класс User описывает пользователя приложения:
- id   — уникальный идентификатор;
- name — имя пользователя.
"""


class User:
    """Информация о пользователе приложения."""

    def __init__(self, user_id: int, name: str) -> None:
        self.id = user_id
        self.name = name

    @property
    def id(self) -> int:
        """Уникальный идентификатор пользователя."""
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Идентификатор пользователя должен быть целым числом")
        if value <= 0:
            raise ValueError("Идентификатор пользователя должен быть положительным")
        self._id = value

    @property
    def name(self) -> str:
        """Имя пользователя."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Имя пользователя должно быть строкой")
        value = value.strip()
        if not value:
            raise ValueError("Имя пользователя не может быть пустым")
        self._name = value

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"

    def __str__(self) -> str:
        return f"{self.name} (id={self.id})"
