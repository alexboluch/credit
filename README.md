## Credit Service API (Django REST Framework)

### Проєкт

Цей репозиторій містить бекенд-сервіс, побудований на **Django REST Framework (DRF)**, призначений для управління фінансовими об'єктами (Кредитами та Платежами). Проєкт повністю контейнеризовано за допомогою **Docker Compose**.

### Стек Технологій

  * **Фреймворк:** Django 5.x
  * **API:** Django REST Framework (DRF)
  * **База даних:** SQLite3 (файл `db.sqlite3`)
  * **Контейнеризація:** Docker та Docker Compose (V2)
  * **Мова:** Python 3.11+

-----

## Розгортання та Запуск (Docker)

Для запуску проєкту потрібні лише встановлені Docker та Docker Compose.

### 1\. Передумови

Переконайтеся, що на вашій системі встановлено:

1.  [Docker Engine](https://docs.docker.com/engine/install/)
2.  [Docker Compose](https://docs.docker.com/compose/install/)

### 2\. Запуск Проєкту

Виконайте ці команди у кореневій папці проєкту:

```bash
# 1. Збірка образу та запуск контейнера у фоновому режимі (-d)
# Ця команда автоматично виконає міграції перед запуском сервера.
docker-compose up --build -d
```

### 3\. Доступ до Сервісу

Після запуску контейнера, API буде доступно локально:

| Опис | URL |
| :--- | :--- |
| **Базовий URL API** | **http://localhost:8000/api/** |

### 4\. Керування Контейнерами

| Дія | Команда |
| :--- | :--- |
| **Зупинити сервіс** | `docker-compose down` |
| **Переглянути логи** | `docker-compose logs -f web` |
| **Виконати команду в контейнері** | `docker-compose exec web bash` (для відкриття терміналу) |

-----

## Розробка та Тестування

### 1\. Виконання Міграцій та Тестів

Ви можете запускати Django-команди безпосередньо в контейнері:

```bash
# Застосування міграцій (якщо змінилася модель)
docker-compose exec web python manage.py migrate product

# Запуск юніт-тестів для додатку 'service_app'
docker-compose exec web python manage.py test product
```

### 2\. Налаштування VS Code для Дебагу (Рекомендовано)

Для покрокового налагодження (debugging) у VS Code:

1.  Встановіть усі необхідні залежності у локальне віртуальне середовище (`venv`).
2.  Переконайтеся, що файли `.vscode/settings.json` та `.vscode/launch.json` налаштовані (ці налаштування фіксують шлях до локального `venv`).
3.  Встановіть точку зупину (Breakpoint) у коді (наприклад, у `product/tests.py`).
4.  На вкладці **Run and Debug** (`Ctrl+Shift+D`) виберіть конфігурацію **`Python: Django Tests (Debug)`** і запустіть її.

-----

## Доступні API Ендпоінти

| Призначення | Метод | URL-префікс |
| :--- | :--- | :--- |
| **Створення Credit** | `POST` | `/api/create_credit/` |
| **Деталі/Оновлення/Видалення** | `GET`/`PUT`/`PATCH`/`DELETE` | `/api/credits/{id}/` |
| **Обробка платежу** | `POST` | `/api/process_payment/` |