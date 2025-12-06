"""
Контроллер для работы с базой данных SQLite в памяти.
"""

from __future__ import annotations
import sqlite3
from typing import Dict, List, Any


class CurrencyRatesCRUD:
    """Обёртка над соединением SQLite с CRUD-операциями."""

    def __init__(self, connection: sqlite3.Connection | None = None) -> None:
        if connection is None:
            self._conn = sqlite3.connect(":memory:")
            self._own_connection = True
        else:
            self._conn = connection
            self._own_connection = False

        self._conn.row_factory = sqlite3.Row

        self._enable_foreign_keys()
        self._create_schema()

    def _enable_foreign_keys(self) -> None:
        cur = self._conn.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")
        self._conn.commit()

    def _create_schema(self) -> None:
        cur = self._conn.cursor()
        cur.executescript(
            """
            CREATE TABLE IF NOT EXISTS user (
                id   INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS currency (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                num_code  TEXT   NOT NULL,
                char_code TEXT   NOT NULL,
                name      TEXT   NOT NULL,
                value     FLOAT,
                nominal   INTEGER
            );

            CREATE TABLE IF NOT EXISTS user_currency (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                currency_id INTEGER NOT NULL,
                FOREIGN KEY(user_id)     REFERENCES user(id),
                FOREIGN KEY(currency_id) REFERENCES currency(id)
            );
            """
        )
        self._conn.commit()


    def _create(self, num_code: str, char_code: str, name: str,
                value: float, nominal: int) -> int:
        """Добавляет валюту и возвращает её ID."""
        sql = """
            INSERT INTO currency (num_code, char_code, name, value, nominal)
            VALUES (?, ?, ?, ?, ?)
        """
        cur = self._conn.cursor()
        cur.execute(sql, (num_code, char_code, name, value, nominal))
        self._conn.commit()
        return cur.lastrowid

    def _read(self) -> List[Dict[str, Any]]:
        """Возвращает список валют."""
        sql = """
            SELECT id, num_code, char_code, name, value, nominal
            FROM currency
            ORDER BY char_code
        """
        cur = self._conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        return [dict(row) for row in rows]

    def _update(self, rate_by_code: Dict[str, float]) -> None:
        """Обновляет курс валют."""
        sql = "UPDATE currency SET value = :value WHERE char_code = :char_code"
        cur = self._conn.cursor()

        for char_code, new_value in rate_by_code.items():
            cur.execute(sql, {"value": new_value, "char_code": char_code})

        self._conn.commit()

    def _delete(self, currency_id: int) -> None:
        """Удаляет валюту по id."""
        sql = "DELETE FROM currency WHERE id = ?"
        cur = self._conn.cursor()
        cur.execute(sql, (currency_id,))
        self._conn.commit()


    def close(self) -> None:
        if self._own_connection:
            self._conn.close()

    def __enter__(self) -> "CurrencyRatesCRUD":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
