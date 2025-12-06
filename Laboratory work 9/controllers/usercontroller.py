from controllers.databasecontroller import CurrencyRatesCRUD
from models.user import User


class UserController:
    """Контроллер для CRUD-операций над пользователями"""

    def __init__(self, db_controller: CurrencyRatesCRUD):
        self.db = db_controller

    def create_user(self, name: str) -> int:
        sql = "INSERT INTO user (name) VALUES (?)"
        cur = self.db.conn.cursor()
        cur.execute(sql, (name,))
        self.db.conn.commit()
        return cur.lastrowid

    def get_user(self, user_id: int):
        sql = "SELECT id, name FROM user WHERE id = ?"
        cur = self.db.conn.cursor()
        cur.execute(sql, (user_id,))
        row = cur.fetchone()
        if row:
            return {"id": row[0], "name": row[1]}
        return None

    def list_users(self):
        sql = "SELECT id, name FROM user"
        cur = self.db.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        return [{"id": r[0], "name": r[1]} for r in rows]

    def update_user(self, user_id: int, name: str):
        sql = "UPDATE user SET name = ? WHERE id = ?"
        cur = self.db.conn.cursor()
        cur.execute(sql, (name, user_id))
        self.db.conn.commit()

    def delete_user(self, user_id: int):
        sql = "DELETE FROM user WHERE id = ?"
        cur = self.db.conn.cursor()
        cur.execute(sql, (user_id,))
        self.db.conn.commit()
