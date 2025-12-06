"""
Пакет моделей предметной области.

Содержит классы:

- Author        — информация об авторе приложения;
- App           — описание приложения и его автора;
- User          — пользователь и его идентификатор;
- Currency      — валюта и её текущий курс;
- UserCurrency  — связь «пользователь ↔ валюта» (подписки на валюты).

Импортируя пакет models, можно сразу получить доступ ко всем моделям:
    from models import Author, App, User, Currency, UserCurrency
"""

from .author import Author
from .app import App
from .user import User
from .currency import Currency
from .user_currency import UserCurrency

__all__ = [
    "Author",
    "App",
    "User",
    "Currency",
    "UserCurrency",
]
