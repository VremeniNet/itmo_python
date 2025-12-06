# Лабораторная работа №8  
## Клиент-серверное приложение на Python с использованием Jinja2
## Желанов Даниил, P4150

---

# 1. Цель работы

Целью лабораторной работы №8 является разработка учебного клиент-серверного приложения без использования сторонних веб-фреймворков. В ходе работы необходимо:

- реализовать собственный HTTP-сервер на основе `HTTPServer` и `BaseHTTPRequestHandler`;
- настроить маршрутизацию запросов;
- разработать модели предметной области (Author, App, User, Currency, UserCurrency);
- подключить шаблонизатор Jinja2 и реализовать отображение данных через HTML-шаблоны;
- получать курсы валют через функцию `get_currencies` и отображать их пользователям;
- сформировать страницы: главная, пользователи, страница пользователя, курсы валют, информация об авторе.

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

Структура проекта соответствует архитектуре MVC и требованиям ЛР8:

myapp/

│

├── models/

│ ├── __init__.py # импорт всех моделей

│ ├── author.py # модель Author

│ ├── app.py # модель App

│ ├── user.py # модель User

│ ├── currency.py # модель Currency

│ ├── user_currency.py # модель UserCurrency

│

├── templates/

│ ├── index.html # главная страница

│ ├── users.html # список пользователей

│ ├── user.html # страница пользователя

│ ├── currencies.html # курсы валют

│ ├── author.html # информация об авторе

│

├── static/

│ ├── style.css # стилизация интерфейса

│
├── utils/

│ ├── currencies_api.py # функция get_currencies

│

├── myapp.py # HTTP-сервер, маршруты, Jinja2

## 4. Описание реализации

### 4.1 Реализация моделей (геттеры/сеттеры)

Все модели находятся в пакете `models/` и реализуют предметную область: `Author`, `App`, `User`, `Currency`, `UserCurrency`.

Каждый класс содержит:
- приватные атрибуты (`_id`, `_name`, `_value` и т.п.);
- геттеры/сеттеры с проверкой типов и корректных значений;
- понятный метод `__repr__` — для удобства отладки.

Например, модель **Currency** содержит строгие проверки курса и номинала:

```python
@property
def value(self) -> float:
    return self._value

@value.setter
def value(self, v: float) -> None:
    if not isinstance(v, (int, float)):
        raise TypeError("Курс валюты должен быть числом")
    if v <= 0:
        raise ValueError("Курс валюты должен быть положительным")
    self._value = float(v)
```

Модель UserCurrency реализует связь “многие-ко-многим” между пользователями и валютами:

```python
@property
def user(self) -> User:
    return self._user

@property
def currency(self) -> Currency:
    return self._currency
```

### 4.2 Маршрутизация и обработка запросов

Сервер построен на стандартных классах `HTTPServer` и `BaseHTTPRequestHandler`.

Основной файл — `myapp.py`.

Маршруты обрабатываются вручную через `self.path` и `urllib.parse`:

```python
def do_GET(self):
    parsed = urlparse(self.path)
    path = parsed.path

    if path.startswith("/static/"):
        self._serve_static(...)
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
```

Каждый маршрут вынесен в отдельный метод `handle_*`.

Например, логика страницы одного пользователя `/user?id=...`:

```python
def handle_user(self, parsed):
    query = parse_qs(parsed.query)
    raw_id = query.get("id", [None])[0]

    user_id = int(raw_id) if raw_id else None
    user_obj = next((u for u in users if u.id == user_id), None)
    if user_obj is None:
        self.handle_not_found()
        return

    subs = [rel for rel in user_currency_relations if rel.user.id == user_id]

    update_currency_rates()

    history_by_code = {
        rel.currency.char_code: build_fake_history_for_currency(rel.currency)
        for rel in subs
    }

    context = {
        "app": app_info,
        "user": user_obj,
        "subscriptions": subs,
        "history_json": json.dumps(history_by_code, ensure_ascii=False),
    }

    self._render("user.html", context)
```

### 4.3 Использование шаблонизатора Jinja2

Jinja2 используется для формирования HTML-страниц. Шаблоны хранятся в директории `templates/`.

Инициализация Jinja2 происходит один раз при старте сервера:

```python
env = Environment(
    loader=FileSystemLoader(str(BASE_DIR / "templates")),
    autoescape=select_autoescape(["html", "xml"]),
)
```

Рендер универсальный:

```python
def _render(self, template_name, context, status=200):
    template = env.get_template(template_name)
    html = template.render(**context)
    self.send_response(status)
    self.send_header("Content-Type", "text/html; charset=utf-8")
    self.end_headers()
    self.wfile.write(html.encode("utf-8"))
```

### 4.4 Интеграция функции get_currencies для получения актуальных курсов

Для получения курсов валют используется API ЦБ РФ. Реализация — в файле:

```python
response = requests.get(url, timeout=5)
data = response.json()
rate = data["Valute"][code]["Value"]
```

Интеграция в приложение - через функцию `update_currency_rates()`:

```python
def update_currency_rates():
    codes = [cur.char_code for cur in currencies]
    rates = get_currencies(codes)

    for cur in currencies:
        if cur.char_code in rates:
            cur.value = rates[cur.char_code]
```
Обновление выполняется:

- при открытии страницы `/currencies`;

- при загрузке `/user?id=...` (перед построением графика).

## 5. Примеры работы приложения

### 5.1. Главная страница (/)

<img width="986" height="700" alt="image" src="https://github.com/user-attachments/assets/62bbd502-65e2-4674-9723-1904a4be1998" />


### 5.2. Список пользователей (/users)

<img width="986" height="566" alt="image" src="https://github.com/user-attachments/assets/24677d26-cceb-41f3-90de-46cc2ef55a0d" />

### 5.3. Список валют (/currencies)

<img width="986" height="603" alt="image" src="https://github.com/user-attachments/assets/bee30caa-9209-4920-809d-55f15909ee4a" />


### 5.4. Страница пользователя (/user?id=1)

<img width="986" height="908" alt="image" src="https://github.com/user-attachments/assets/5700e870-97a3-46bb-9fb1-21750606a88c" />


### 5.4. Страница автора (/author)

<img width="985" height="573" alt="image" src="https://github.com/user-attachments/assets/bbc2899d-7691-4dab-937f-3ef73ce27e6b" />

## 6. Описание самостоятельной работы

В рамках самостоятельной части лабораторной работы была реализована функциональность отображения
графика изменения курсов валют, на которые подписан пользователь. График встроен в страницу
`/user?id=...` и отображает динамику значений за последние 3 месяца.

### 6.1 Выбор подхода к построению графика

Так как API ЦБ РФ предоставляет только текущий курс валюты, а не историю за несколько месяцев,
необходимо было выбрать подход:

1. полностью реальная история — требуется хранить курсы в базе данных или файлах ежедневно;
2. частично реальная история — комбинировать текущие данные и псевдо-историю;
3. полностью псевдореальная история — генерация значений на основе текущего курса.

В учебных условиях был выбран **вариант 3**, поскольку он позволяет показать:
- интеграцию данных с бэкенда в шаблон,
- рендеринг графика в браузере через JavaScript,
- обработку нескольких валют одновременно.

### 6.2 Генерация динамики курсов

Для каждой валюты создаётся массив из 90 значений (3 месяца).  
Начальная точка генерируется близко к текущему курсу, затем применяется небольшое случайное движение:

```python
# myapp.py — генерация 90 дней истории
history_by_code = {
    rel.currency.char_code: build_fake_history_for_currency(rel.currency)
    for rel in subs
}
```

Где функция строит псевдореальные данные:

```python
history = []
current = currency.value
for i in range(90):
    delta = random.uniform(-0.5, 0.5)
    current = max(1.0, current + delta)
    history.append(round(current, 2))
```

Готовая структура передаётся в шаблон в формате JSON:

```python
context = {
    "user": user_obj,
    "subscriptions": subs,
    "history_json": json.dumps(history_by_code, ensure_ascii=False),
}
```

### 6.3 Встраивание графика на страницу пользователя

На странице `templates/user.html` подключена библиотека Chart.js и реализовано построение графика:

```python
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
const history = {{ history_json | safe }};
...
new Chart(ctx, {
    type: 'line',
    data: {
        labels: labels,
        datasets: datasets,
    }
});
</script>
```
График строит несколько линий одновременно, по одной для каждой валюты, на которую подписан пользователь.

## 7. Тестирование

В рамках лабораторной работы была выполнена серия тестов, направленных на проверку корректности
работы моделей, функции `get_currencies`, а также базовой серверной логики.  
Тестирование проводилось с использованием модуля `unittest`.

---

### 7.1 Тестирование моделей

Каждая модель (`User`, `Currency`, `UserCurrency`, `App`, `Author`) содержит геттеры и сеттеры
с валидацией типов и значений.  
Основные проверки:

- корректная установка допустимых значений;
- выброс исключений при ошибочных данных;
- корректная работа свойств после изменения.

Пример теста для модели `Currency`:

```python
def test_currency_setters(self):
    c = Currency(1, 840, "USD", "Доллар США", value=90.5, nominal=1)
    self.assertEqual(c.value, 90.5)

    c.value = 91.7
    self.assertEqual(c.value, 91.7)

    with self.assertRaises(ValueError):
        c.value = -10  # отрицательный курс — ошибка
```

Пример теста для модели `User`:

```python
def test_user_name_validation(self):
    u = User(1, "Иван")
    self.assertEqual(u.name, "Иван")

    with self.assertRaises(ValueError):
        User(2, "")  # пустое имя недопустимо
```

Результат выполнения тестов:

<img width="396" height="170" alt="image" src="https://github.com/user-attachments/assets/676844ea-ff38-4188-b71e-13b8b313ce54" />


### 7.2 Тестирование функции `get_currencies`

Функция получает курс валют через API и обрабатывает ошибки:

- сетевые ошибки (ConnectionError),

- некорректный JSON (ValueError),

- отсутствие нужной валюты (KeyError).

Тесты имитируют разные сценарии:

```python
def test_currency_usd_real_rate(self):
    data = get_currencies(["USD"])
    self.assertIn("USD", data)
    self.assertIsInstance(data["USD"], float)
    self.assertGreaterEqual(data["USD"], 0)
```

Проверка отсутствующей валюты:
```python
def test_nonexistent_code_raises_key_error(self):
    with self.assertRaises(KeyError):
        get_currencies(["XYZ"])
```

Проверка неправильного URL:
```python
def test_connection_error_wrong_url(self):
    with self.assertRaises(ConnectionError):
        get_currencies(["USD"], url="https://")
```

Некорректный JSON:
```python
def test_invalid_json(self):
    with self.assertRaises(ValueError):
        get_currencies(["USD"], url="https://example.com")
```

Результат выполнения тестов:

<img width="362" height="174" alt="image" src="https://github.com/user-attachments/assets/27f8a625-94a1-4beb-be7c-18b66d249667" />

## 8. Выводы

### Какие проблемы возникли при реализации

В процессе разработки приложения возникло несколько характерных сложностей:

1. **Корректная работа get_currencies с API ЦБ РФ**  
   При интеграции функции пришлось учитывать множество исключений: недоступность API, некорректный JSON, отсутствие нужных валют. Это потребовало тщательной обработки ошибок и тестов.

2. **Строгие проверки моделей (валидаторы в сеттерах)**  
   Модели требовали строгой типизации и проверки данных. На этапе создания тестовых данных возникали ошибки, связанные с тем, что Currency не допускает нулевые и отрицательные значения, что потребовало корректной инициализации.

3. **Маршрутизация через BaseHTTPRequestHandler**  
   В отличие от современных фреймворков, у стандартного HTTPServer нет роутера. Маршруты приходилось разбирать вручную через `self.path` и `urllib.parse`, что увеличило объём кода и необходимость чёткого контроля URL.

4. **Работа Jinja2 внутри чистого Python-сервера**  
   Потребовалось правильно настроить `Environment` и систему шаблонов, чтобы шаблоны подгружались один раз и могли многоразово использоваться.

5. **Самостоятельная часть — график динамики валют**  
   Настоящий исторический API недоступен напрямую в рамках стандарта ЦБ РФ, поэтому пришлось имитировать данные или использовать внешние источники.

---

### Как удалось применить принципы MVC

Проект был структурирован в соответствии с архитектурой MVC:

- **Models** — объектные классы User, Currency, App, UserCurrency, содержащие данные и строгие валидаторы.  
- **Views** — шаблоны Jinja2 (HTML-файлы), обеспечивающие оформление данных без бизнес-логики.  
- **Controller** — файл `myapp.py`, который обрабатывает HTTP-запросы, вызывает модели, рендерит HTML и отправляет клиенту результат.


---

### Что нового узнали о работе с HTTPServer, Jinja2 и API курсов валют

1. **HTTPServer**  
   - Позволяет поднять полностью рабочий сервер без фреймворков.  
   - Требует явного описания маршрутов и ручной обработки путей.  
   - Хорошо подходит для учебных целей и демонстрации внутренних механизмов веб-сервера.

2. **Jinja2**  
   - Удобен для отделения логики от представления.  
   - Поддерживает наследование шаблонов, циклы, условия.  
   - Может быть эффективно использован даже без Flask или Django.

3. **API курсов валют**  
   - ЦБ РФ предоставляет открытое API в формате JSON, которое можно легко интегрировать.  
   - Возникает необходимость обработки сетевых ошибок и проверок структуры данных.  
   - Понял, как использовать внешние API в серверных приложениях и правильно валидировать ответы.

---

В итоге лабораторная работа позволила закрепить навыки работы с сетевой логикой, шаблонизатором Jinja2, архитектурой MVC и внешними API, а также потренировать построение клиент-серверных приложений без использования больших фреймворков.

