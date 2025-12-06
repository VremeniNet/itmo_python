from controllers.databasecontroller import CurrencyRatesCRUD


class UserCurrencyController:
    """Контроллер для подписок пользователя на валюты"""

    def __init__(self, db_controller: CurrencyRatesCRUD):
        self.db = db_controller

    def subscribe(self, user_id: int, currency_id: int) -> int:
        sql = "INSERT INTO user_currency (user_id, currency_id) VALUES (?, ?)"
        cur = self.db.conn.cursor()
        cur.execute(sql, (user_id, currency_id))
        self.db.conn.commit()
        return cur.lastrowid

    def get_user_subscriptions(self, user_id: int):
        sql = """
            SELECT uc.id, c.id, c.char_code, c.name, c.value, c.nominal
            FROM user_currency uc
            JOIN currency c ON uc.currency_id = c.id
            WHERE uc.user_id = ?
        """
        cur = self.db.conn.cursor()
        cur.execute(sql, (user_id,))
        rows = cur.fetchall()

        return [
            {
                "subscription_id": r[0],
                "currency_id": r[1],
                "char_code": r[2],
                "currency_name": r[3],
                "value": r[4],
                "nominal": r[5]
            }
            for r in rows
        ]

    def unsubscribe(self, subscription_id: int):
        sql = "DELETE FROM user_currency WHERE id = ?"
        cur = self.db.conn.cursor()
        cur.execute(sql, (subscription_id,))
        self.db.conn.commit()
