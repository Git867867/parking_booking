# Отчёт по ПР10 — Parking Booking

## 1. Тема и цель
Административная панель Django и работа с данными через ORM на примере
системы бронирования парковочных мест Parking Booking.

## 2. Задания Яндекс Практикума
Блоки «Админ-зона Django», «Django ORM. Получение информации из БД»,
«Финальный проект спринта: Блогикум». Приёмы перенесены в свою предметную
область без копирования учебных моделей. [скриншоты]

## 3. Административная панель
Зарегистрированы Spot, User, Booking. Настроены list_display, list_display_links,
search_fields, list_filter, ordering, list_per_page=20, list_editable (daily_rate),
readonly_fields (id), help_text, TabularInline, метод-столбец spot_rate,
аннотация active_bookings, list_select_related, actions, date_hierarchy,
autocomplete_fields. Локализация: AppConfig.verbose_name, Meta.verbose_name,
LANGUAGE_CODE="ru-ru". Права: группа «Parking Operators», staff operator. [скриншоты]

## 4. Модели, миграции, менеджер
Booking.Status (TextChoices); миграция данных 0003 переносит is_cancelled -> status,
0004 удаляет старое поле. BookingQuerySet + BookingManager: active(), cancelled(),
completed(), for_date(). Spot: help_text, GeneratedField is_expensive, slug
(миграции 0004-0006), save() с транслитерацией, get_absolute_url().

## 5. ORM-запросы
booking_list: active() + фильтры + annotate(F) + values() + сортировка по белому
списку + Paginator(5). booking_detail: select_related. statistics: aggregate(Count
с Q по трём статусам) и групповая статистика по местам. Свободные места:
active().for_date(дата) -> exclude(pk__in=...).

## 6. Доступность мест
Активная бронь блокирует место на дату; отменённая и завершённая — нет.
Подтверждено тестами и вручную. [скриншоты]

## 7. Анализ SQL (Debug Toolbar)
Список броней: основной запрос с JOIN, справочники мест/пользователей, COUNT
для пагинации — ожидаемы. Карточка брони: один запрос с JOIN (select_related).
Проблема N+1 отсутствует. [скриншоты SQL]

## 8. Проверки
manage.py check — без ошибок; makemigrations --check — изменений нет;
pytest -v — 15 тестов passed. [скриншот терминала]

## 9. Git
Коммит: [хэш] «ПР10: админ-панель, ORM, статусы, slug, GeneratedField, Debug Toolbar».

## 10. Выводы
Админ-панель настроена, ORM-запросы проверены, бизнес-правило доступности
соблюдается по статусу ACTIVE, документация актуальна. Ограничение: admin не
заменяет бизнес-проверки при создании конфликтующих броней.