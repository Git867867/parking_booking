# Parking Booking — ПР10 (Django Admin и ORM)

Система бронирования парковочных мест. Административная панель, статусы
бронирований (TextChoices), slug страниц мест, GeneratedField, контекстный
процессор и анализ SQL через Django Debug Toolbar.

## Модели

- `Spot`: number, covered, daily_rate (help_text), is_expensive (GeneratedField:
  daily_rate >= 500, хранится в БД), slug (unique, формируется автоматически),
  метод get_absolute_url().
- `User`: name, phone — пользователь предметной области (не учётная запись Django).
- `Booking`: spot/user (ForeignKey, PROTECT, related_name="bookings"), start, end,
  status (ACTIVE / CANCELLED / COMPLETED). Менеджер: active(), cancelled(),
  completed(), for_date(дата). Метод cancel() меняет статус, запись не удаляется.

## Миграции

- bookings: 0002 — поле status; 0003 — перенос данных is_cancelled -> status
  (обратимая миграция данных); 0004 — удаление is_cancelled.
- spots: 0002 — help_text; 0003 — GeneratedField; 0004 — slug; 0005 — заполнение
  slug; 0006 — unique=True.

## Админ-панель

- SpotAdmin: столбцы, поиск по номеру, фильтр по типу, list_editable (daily_rate),
  readonly id, inline бронирований, аннотация числа активных броней,
  ссылка «Посмотреть на сайте».
- UserAdmin: поиск по имени и телефону, inline бронирований.
- BookingAdmin: поиск по связанным полям, фильтры по дате и статусу, date_hierarchy,
  autocomplete_fields, list_select_related, действия «Отменить» и «Вернуть в активные».

## Страницы

- `/` — главная
- `/spots/` — список: фильтр по типу, поиск, сортировка
- `/spots/<slug>/` — карточка места по slug
- `/spots/available/?date=ГГГГ-ММ-ДД` — свободные места (блокирует только ACTIVE)
- `/bookings/` — активные брони: фильтры, сортировка, пагинация по 5
- `/bookings/<id>/` — карточка брони (select_related)
- `/bookings/statistics/` — статистика по статусам и по местам
- `/admin/` — административная панель
- `/__debug__/` — Debug Toolbar (только DEBUG=True)

## Тестовые данные

`create_test_data.py` (идемпотентен): 6 мест, 3 пользователя, 12 бронирований
(8 активных, 2 отменённых, 2 завершённых), группа «Parking Operators»
(view/add/change места, без delete) и staff-пользователь operator / Operator#2026pass.

## Запуск

    python -m venv venv
    .\venv\Scripts\python.exe -m pip install -r requirements.txt
    .\venv\Scripts\python.exe manage.py migrate
    .\venv\Scripts\python.exe create_test_data.py
    .\venv\Scripts\python.exe manage.py createsuperuser
    .\venv\Scripts\python.exe manage.py runserver

## Автор

Магомерзаев А.Р., ЭФБО-13-24