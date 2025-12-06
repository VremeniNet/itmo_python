"""
myapp.py — точка входа приложения (Лабораторная работа №8).

Отвечает за:
- запуск HTTP-сервера;
- маршрутизацию запросов;
- работу с шаблонизатором Jinja2;
- получение курсов валют через get_currencies и отображение пользователям.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path
from typing import Dict, List


from jinja2 import Environment, FileSystemLoader, select_autoescape

from models import Author, App, User, Currency, UserCurrency
from utils.currencies_api import get_currencies



BASE_DIR = Path(__file__).resolve().parent

env = Environment(
    loader=FileSystemLoader(str(BASE_DIR / "templates")),
    autoescape=select_autoescape(["html", "xml"]),
)

author = Author("Даниил Желанов", "P4150")
app_info = App("Currency Tracker", "1.0.0", author)

users: List[User] = [
    User(1, "Алиса"),
    User(2, "Боб"),
]

currencies: List[Currency] = [
    Currency(1, 840, "USD", "Доллар США", value=0.0, nominal=1),
    Currency(2, 978, "EUR", "Евро", value=0.0, nominal=1),
    Currency(3, 826, "GBP", "Фунт стерлингов", value=0.0, nominal=1),
]

user_currency_relations: List[UserCurrency] = [
    UserCurrency(1, users[0], currencies[0], is_active=True, alias="Зарплата"),
    UserCurrency(2, users[0], currencies[1], is_active=True, alias=None),
    UserCurrency(3, users[1], currencies[2], is_active=True, alias="Путешествия"),
]


def build_user_subscriptions() -> Dict[int, List[UserCurrency]]:
    """
    Возвращает словарь user_id -> список подписок (UserCurrency).
    """
    mapping: Dict[int, List[UserCurrency]] = {}
    for rel in user_currency_relations:
        mapping.setdefault(rel.user.id, []).append(rel)
    return mapping


def update_currency_rates() -> None:
    """
    Обновляет значение value у Currency с помощью функции get_currencies.
    """
    codes = [cur.char_code for cur in currencies]
    try:
        rates = get_currencies(codes)
    except Exception:
        return

    for cur in currencies:
        if cur.char_code in rates:
            cur.value = rates[cur.char_code]



class MyRequestHandler(BaseHTTPRequestHandler):
    """Обработчик HTTP-запросов приложения."""


    def _render(self, template_name: str, context: dict, status: int = 200) -> None:
        """Рендерит шаблон и отправляет HTML-ответ."""
        template = env.get_template(template_name)
        html = template.render(**context)

        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def _serve_static(self, path: str) -> None:
        static_root = BASE_DIR / "static"
        file_path = static_root / path.lstrip("/")

        if not file_path.is_file():
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")
            return

        if file_path.suffix == ".css":
            content_type = "text/css; charset=utf-8"
        else:
            content_type = "application/octet-stream"

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.end_headers()
        self.wfile.write(file_path.read_bytes())


    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path

        if path.startswith("/static/"):
            self._serve_static(path.replace("/static/", "", 1))
            return

        if path == "/":
            self.handle_index()
        elif path == "/users":
            self.handle_users()
        elif path == "/user":
            self.handle_user(parsed)
        elif path == "/currencies":
            self.handle_currencies()
        elif path == "/author":
            self.handle_author()
        else:
            self.handle_not_found()


    def handle_index(self) -> None:
        context = {"app": app_info}
        self._render("index.html", context)

    def handle_users(self) -> None:
        context = {
            "app": app_info,
            "users": users,
            "user_subscriptions": build_user_subscriptions(),
        }
        self._render("users.html", context)

    def handle_user(self, parsed) -> None:
        query = parse_qs(parsed.query)
        raw_id = query.get("id", [None])[0]

        try:
            user_id = int(raw_id) if raw_id is not None else None
        except ValueError:
            user_id = None

        user_obj = next((u for u in users if u.id == user_id), None)
        if user_obj is None:
            self.handle_not_found()
            return

        subs = [rel for rel in user_currency_relations if rel.user.id == user_obj.id]

        context = {
            "app": app_info,
            "user": user_obj,
            "subscriptions": subs,
        }
        self._render("user.html", context)

    def handle_currencies(self) -> None:
        """Маршрут /currencies — список валют с текущими курсами."""
        update_currency_rates()
        context = {
            "app": app_info,
            "currencies": currencies,
            "rates_date": None,
        }
        self._render("currencies.html", context)

    def handle_author(self) -> None:
        context = {"app": app_info}
        self._render("author.html", context)

    def handle_not_found(self) -> None:
        self.send_response(404)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"<h1>404 Not Found</h1>")


def run(host: str = "127.0.0.1", port: int = 8000) -> None:
    """Запускает HTTPServer с обработчиком."""
    server_address = (host, port)
    httpd = HTTPServer(server_address, MyRequestHandler)
    print(f"Server is running at http://{host}:{port}/")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
