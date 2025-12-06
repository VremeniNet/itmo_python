"""
Связь пользователь ↔ валюта.

Класс UserCurrency описывает, какую валюту отслеживает конкретный пользователь.

Поля:
- id         — уникальный идентификатор связи;
- user       — объект User;
- currency   — объект Currency;
- is_active  — флаг активности подписки;
- alias      — пользовательское название для валюты (опционально).
"""

from .user import User
from .currency import Currency


class UserCurrency:
    """Подписка пользователя на конкретную валюту."""

    def __init__(
        self,
        relation_id: int,
        user: User,
        currency: Currency,
        is_active: bool = True,
        alias: str | None = None,
    ) -> None:
        self.id = relation_id
        self.user = user
        self.currency = currency
        self.is_active = is_active
        self.alias = alias


    @property
    def id(self) -> int:
        """Уникальный идентификатор связи."""
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Идентификатор связи должен быть целым числом")
        if value <= 0:
            raise ValueError("Идентификатор связи должен быть положительным")
        self._id = value


    @property
    def user(self) -> User:
        """Пользователь, подписанный на валюту."""
        return self._user

    @user.setter
    def user(self, value: User) -> None:
        if not isinstance(value, User):
            raise TypeError("user должен быть экземпляром класса User")
        self._user = value


    @property
    def currency(self) -> Currency:
        """Отслеживаемая валюта."""
        return self._currency

    @currency.setter
    def currency(self, value: Currency) -> None:
        if not isinstance(value, Currency):
            raise TypeError("currency должен быть экземпляром класса Currency")
        self._currency = value


    @property
    def is_active(self) -> bool:
        """Флаг активности подписки на валюту."""
        return self._is_active

    @is_active.setter
    def is_active(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError("is_active должен быть булевым значением")
        self._is_active = value


    @property
    def alias(self) -> str | None:
        """Произвольное название валюты, заданное пользователем (опционально)."""
        return self._alias

    @alias.setter
    def alias(self, value: str | None) -> None:
        if value is None:
            self._alias = None
            return

        if not isinstance(value, str):
            raise TypeError("alias должен быть строкой или None")

        trimmed = value.strip()
        self._alias = trimmed or None


    def __repr__(self) -> str:
        return (
            "UserCurrency(id={id!r}, user={user!r}, currency={cur!r}, "
            "is_active={active!r}, alias={alias!r})"
        ).format(
            id=self.id,
            user=self.user,
            cur=self.currency,
            active=self.is_active,
            alias=self.alias,
        )

    def __str__(self) -> str:
        base = f"{self.user.name} → {self.currency.char_code}"
        if self.alias:
            base += f" ({self.alias})"
        return base
