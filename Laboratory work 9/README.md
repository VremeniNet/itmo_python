# Лабораторная работа №9
## CRUD для приложения отслеживания курсов валют c SQLite базой данных
## Желанов Даниил, P4150

# 1. Цель работы

Цель данной лабораторной работы — разработать модульную серверную часть приложения с использованием базы данных SQLite и архитектуры MVC.  
В рамках выполнения необходимо:

1. Реализовать полный набор CRUD-операций (Create, Read, Update, Delete) для сущности *Currency*, обеспечив корректную работу бизнес-логики и безопасность SQL-запросов.
2. Освоить работу с базой данных SQLite, размещённой в памяти (`:memory:`), а также организацию структуры таблиц с использованием первичных (PRIMARY KEY) и внешних ключей (FOREIGN KEY).
3. Понять назначение первичных и внешних ключей и их роль в связях между таблицами.
4. Разделить приложение на уровни модели, контроллеров и представлений, выделив отдельные модули для работы с БД и рендеринга страниц.
5. Научиться использовать архитектуру MVC и обеспечивать корректное разделение ответственности между компонентами.
6. Реализовать вывод таблицы валют пользователю на основе данных, загружаемых и обновляемых через SQL-интерфейс.
7. Создать роутер, обрабатывающий GET-запросы, выполняющий сохранение и обновление данных и вызывающий рендеринг HTML-страниц.
8. Освоить тестирование функциональности модели и контроллера (*currency* и *user*) с помощью библиотеки `unittest.mock`.

---

# 2. Описание предметной области

Предметная область состоит из следующих сущностей:

### **1. Author**
Описание автора приложения.
- `name` — имя автора;
- `group` — учебная группа.

### **2. App**
Модель приложения.
- `name` — название приложения;
- `version` — версия приложения;
- `author` — объект типа `Author`.

### **3. User**
Описание пользователя.
- `id` — уникальный идентификатор;
- `name` — имя пользователя.

### **4. Currency**
Описание валюты.
- `id` — уникальный идентификатор;
- `num_code` — цифровой код валюты;
- `char_code` — символьный код (например, USD, EUR);
- `name` — название;
- `value` — текущий курс (в рублях);
- `nominal` — номинал (за сколько единиц валюты указан курс).

### **5. UserCurrency**
Связь «пользователь — валюта».
- `id` — идентификатор связи;
- `user` — объект `User`;
- `currency` — объект `Currency`;
- `is_active` — активна ли подписка;
- `alias` — пользовательское название подписки.

Связь является отношением «многие ко многим», т.к.:
- один пользователь может быть подписан на несколько валют;
- одна валюта может использоваться несколькими пользователями.

---

# 3. Структура проекта

Структура проекта соответствует архитектуре MVC и требованиям ЛР9:

project/

│

├── controllers/

│   ├── databasecontroller.py     # CRUD-операции через SQLite

│   ├── currencycontroller.py     # Логика управления валютами

│   └── usercontroller.py         # Логика для Users

│

├── models/

│   ├── currency.py               # Модель Currency

│   ├── user.py                   # Модель User

│   ├── user_currency.py          # Связующая Many-to-Many

│   ├── author.py                 # Модель Author

│   ├── app.py                    # Модель App

│   └── __init__.py               # Экспорт моделей

│

├── templates/

│   ├── index.html                # Главная страница

│   ├── users.html                # Список пользователей

│   ├── user.html                 # Страница одного пользователя

│   ├── currencies.html           # Таблица валют

│   └── author.html               # Информация об авторе

│

├── static/

│   └── style.css                 # Стилизация

│

├── utils/

│   └── currencies_api.py         # Получение данных курсов валют

│

├── dem.py                        # Тестовый файл для CRUD

└── myapp.py                      # Роутер, HTTPServer, рендеринг

---

# 4. Реализация CRUD с примерами SQL-запросов

## 4.1. CREATE

```python
sql = """
    INSERT INTO currency (num_code, char_code, name, value, nominal)
    VALUES (?, ?, ?, ?, ?)
"""
cur = self._conn.cursor()
cur.execute(sql, (num_code, char_code, name, value, nominal))
self._conn.commit()
return cur.lastrowid

```

## 4.2. READ

```python
sql = """
        SELECT id, num_code, char_code, name, value, nominal
        FROM currency
        ORDER BY char_code
"""
cur = self._conn.cursor()
cur.execute(sql)
rows = cur.fetchall()
return [dict(row) for row in rows]
```

## 4.3. UPDATE

```python
sql = "UPDATE currency SET value = :value WHERE char_code = :char_code"
cur = self._conn.cursor()

for char_code, new_value in rate_by_code.items():
  cur.execute(sql, {"value": new_value, "char_code": char_code})

self._conn.commit()
```

## 4.4. DELETE

```python
sql = "DELETE FROM currency WHERE id = ?"
cur = self._conn.cursor()
cur.execute(sql, (currency_id,))
self._conn.commit()
```

## 5. Примеры работы приложения

### 5.1. Главная страница (/)

<img width="1049" height="735" alt="image" src="https://github.com/user-attachments/assets/077a4e7d-e7c5-4275-aed7-679bbef19780" />

### 5.2. Список пользователей (/users)

<img width="1050" height="622" alt="image" src="https://github.com/user-attachments/assets/7716b2ec-061e-42f5-b11b-8f6cd846e4c6" />


### 5.3. Список валют (/currencies)

<img width="1050" height="741" alt="image" src="https://github.com/user-attachments/assets/a6f34ea1-040d-476f-ad52-023a12b0f849" />


### 5.4. Страница пользователя (/user?id=1)

<img width="1050" height="911" alt="image" src="https://github.com/user-attachments/assets/bee902b6-c1a2-4586-ac2b-f50b54c2b83c" />


### 5.4. Страница автора (/author)

<img width="1051" height="690" alt="image" src="https://github.com/user-attachments/assets/79f9572c-d6f2-42f2-972d-50dd35304184" />

# 6. Примеры тестов с unittest.mock и результаты их выполнения

В данной лабораторной работе необходимо протестировать работу контроллеров и модели, используя модуль `unittest.mock`.  
Основная цель — проверить корректность взаимодействия контроллера с уровнем доступа к данным (DatabaseController), не обращаясь к реальной базе SQLite.

Для тестирования берём пример с сущностью **Currency**.

---

## 6.1. Тестирование метода list_currencies()

Контроллер должен корректно вызывать метод `_read()` у DatabaseController и возвращать список валют.

```python
import unittest
from unittest.mock import MagicMock

from controllers.currencycontroller import CurrencyController

class TestCurrencyController(unittest.TestCase):
    def test_list_currencies(self):
        # Создаём заглушку базы данных
        mock_db = MagicMock()
        mock_db._read.return_value = [
            {"id": 1, "char_code": "USD", "value": 90.0}
        ]

        controller = CurrencyController(mock_db)

        # Выполняем тестируемый метод
        result = controller.list_currencies()

        # Проверяем корректность результата
        self.assertEqual(result[0]["char_code"], "USD")
        self.assertEqual(result[0]["value"], 90.0)

        # Проверяем, что _read() был вызван ровно один раз
        mock_db._read.assert_called_once()
```
## 6.2. Тестирование операции CREATE

Проверяем, что контроллер корректно вызывает метод `_create()` в DatabaseController.

```python
def test_add_currency(self):
    mock_db = MagicMock()
    mock_db._create.return_value = 10

    controller = CurrencyController(mock_db)
    new_id = controller.add_currency("840", "USD", "Доллар США", 95.7, 1)

    self.assertEqual(new_id, 10)
    mock_db._create.assert_called_once()
```

## 6.3. Тестирование операции UPDATE

```python
def test_update_currency(self):
    mock_db = MagicMock()

    controller = CurrencyController(mock_db)
    controller.update_currency("USD", 99.9)

    mock_db._update.assert_called_once_with({
        "char_code": "USD",
        "value": 99.9
    })
```

## 6.4. Тестирование операции DELETE

```python
def test_delete_currency(self):
    mock_db = MagicMock()

    controller = CurrencyController(mock_db)
    controller.delete_currency(5)

    mock_db._delete.assert_called_once_with(5)
```

## 6.5. Результаты ьестирования

```
Ran 4 tests in 0.001s

OK
```

# 7. Выводы

В ходе выполнения лабораторной работы были реализованы ключевые элементы архитектуры MVC, работа с базой данных SQLite, обработка HTTP-маршрутов и рендеринг HTML-шаблонов. Ниже приведены основные выводы.

## 1. Применение архитектуры MVC

Архитектура MVC позволила разделить приложение на три логических слоя:

- **Models** — содержат представление сущностей (Currency, User, UserCurrency), их свойства, валидацию и логику работы с данными.
- **Controllers** — реализуют бизнес-логику: выполнение CRUD-операций, взаимодействие с базой данных, преобразование данных.
- **Views** — шаблоны Jinja2, отвечающие только за визуальное отображение информации.

Такое разделение существенно упрощает поддержку проекта, повышает читаемость кода и позволяет тестировать контроллеры изолированно от базы данных.

## 2. Работа с SQLite

В работе был создан собственный слой доступа к данным — `DatabaseController`, который:

- создаёт таблицы (`user`, `currency`, `user_currency`);
- выполняет CRUD-операции с использованием **параметризированных SQL-запросов**;
- обеспечивает защиту от SQL-инъекций;
- хранит всю логику работы с SQLite отдельно от моделей и контроллеров.

Работа с базой в оперативной памяти (`sqlite3.connect(':memory:')`) позволила быстро тестировать приложение без необходимости настройки внешней среды.

## 3. Обработка HTTP-маршрутов

Сервер был реализован на основе `HTTPServer` и `BaseHTTPRequestHandler`, что позволило понять:

- как устроена ручная маршрутизация (`do_GET`, `urlparse`, `parse_qs`);
- как сервер выбирает нужный обработчик URL;
- как формируются и отправляются HTTP-ответы (статус, заголовки, тело ответа).

Поддержаны маршруты:

- `/` — главная страница;
- `/users` — список пользователей;
- `/user?id=...` — просмотр конкретного пользователя;
- `/currencies` — текущие курсы валют;
- `/author` — информация об авторе.

Таким образом, была смоделирована работа настоящего веб-приложения.

## 4. Рендеринг шаблонов Jinja2

В проекте использовался шаблонизатор Jinja2:

- шаблоны хранятся в каталоге *templates/*;
- объект `Environment` создаётся один раз при старте приложения;
- контроллеры передают данные в шаблоны через словарь контекста;
- применяются такие функции Jinja2, как циклы, условия, фильтры, вложенные переменные.

Особенно важным стало соединение Jinja2 с Python-логикой: данные, полученные через контроллеры, автоматически подставляются в HTML.

## 5. Общий итог

В результате выполнения лабораторной работы были освоены:

- основы архитектуры MVC;
- практическая работа с SQLite и SQL-запросами;
- обработка HTTP-маршрутов в собственном минимальном фреймворке;
- рендеринг динамических HTML-страниц с использованием Jinja2;
- применение `unittest.mock` для тестирования контроллеров без обращения к реальной базе.

Полученный опыт позволяет лучше понимать принципы работы веб-фреймворков (Flask, Django, FastAPI) и формирует базовый фундамент для перехода к промышленным технологиям.
