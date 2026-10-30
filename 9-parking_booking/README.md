# Parking Booking — система бронирования парковочных мест

Веб-приложение на Django для управления парковочными местами и бронированиями. ПР9: слой доступа к данным переведён с ручных SQL-запросов и библиотеки sqlite3 на Django ORM.

## Технологии

- Python 3
- Django 5.1+
- SQLite (доступ к данным через Django ORM)

## Модели данных

- `Spot` — парковочные места; поля: `number`, `covered`, `daily_rate`
- `User` — пользователи; поля: `name`, `phone`
- `Booking` — бронирования; поля: `start`, `end`, `is_cancelled`; связи: `ForeignKey` на `Spot` и `User` с `on_delete=PROTECT` и `related_name="bookings"`

## Запуск проекта

1. Клонируйте репозиторий:
   `git clone <адрес репозитория>`
2. Создайте и активируйте виртуальное окружение:
   `python -m venv venv`
   `venv\Scripts\activate`
3. Установите зависимости:
   `pip install -r requirements.txt`
4. Создайте и примените миграции:
   `python manage.py makemigrations`
   `python manage.py migrate`
5. Запустите сервер разработки:
   `python manage.py runserver`
6. Откройте в браузере: `http://127.0.0.1:8000/`

## Перенос данных из базы ПР7

Исходная база ПР7 хранится в `data/parking.sqlite` и не изменяется. Django использует целевую базу `db.sqlite3`.

1. Инспекция исходной базы:
   `python db/inspect_source_db.py`
2. Перенос данных в целевую базу (после применения миграций):
   `python db/import_sqlite_to_orm.py`

## Реализованные страницы

- `/` — главная страница
- `/spots/` — список мест: фильтрация по типу, поиск по номеру (`icontains`)
- `/spots/<id>/` — карточка места (`get_object_or_404`), статус на сегодня
- `/spots/available/` — поиск свободных мест на дату (`exclude`)
- `/bookings/` — список бронирований: фильтры по дате, месту, пользователю, поиск по связанным полям (`q`, `spot_number`, `user_name`), сортировка, пагинация (`Paginator`, `{% querystring %}`)
- `/bookings/<id>/` — карточка бронирования (`select_related`)
- `/bookings/statistics/` — статистика (`annotate`, `Count`, `Q`, `aggregate`, `Avg`, `Max`)

## Структура проекта

- `parking/` — настройки проекта
- `homepage/` — главная страница
- `spots/` — модели и представления парковочных мест
- `users/` — модель пользователя
- `bookings/` — модели и представления бронирований
- `templates/` — HTML-шаблоны страниц
- `db/` — скрипты инспекции и переноса данных из базы ПР7
- `sql/` — SQL-слой ПР7 (сохранён как предыдущая реализация, представления его не используют)
- `data/` — исходная база ПР7 `parking.sqlite`

## Автор

<имя, группа>
