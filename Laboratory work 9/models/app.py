"""
Модель приложения.

Класс App хранит базовую информацию о приложении:
- name    — название;
- version — строка версии;
- author  — объект Author (см. models.author).
"""

from .author import Author


class App:
    """Описание приложения и его автора."""

    def __init__(self, name: str, version: str, author: Author) -> None:
        self.name = name
        self.version = version
        self.author = author

    @property
    def name(self) -> str:
        """Название приложения."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Название приложения должно быть строкой")
        value = value.strip()
        if not value:
            raise ValueError("Название приложения не может быть пустым")
        self._name = value

    @property
    def version(self) -> str:
        """Версия приложения (строка, например '1.0.0')."""
        return self._version

    @version.setter
    def version(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Версия приложения должна быть строкой")
        value = value.strip()
        if not value:
            raise ValueError("Версия приложения не может быть пустой")
        self._version = value

    @property
    def author(self) -> Author:
        """Объект Author, описывающий автора приложения."""
        return self._author

    @author.setter
    def author(self, value: Author) -> None:
        if not isinstance(value, Author):
            raise TypeError("author должен быть экземпляром класса Author")
        self._author = value

    def __repr__(self) -> str:
        return (
            f"App(name={self.name!r}, version={self.version!r}, "
            f"author={self.author!r})"
        )
