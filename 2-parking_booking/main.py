"""Точка запуска системы бронирования парковочных мест."""

from bookings import (
    cancel_booking,
    create_booking,
    get_booking_status,
    is_spot_available,
)
from spots import find_spot_by_id, sort_spots_by_price
from storage import load_bookings, load_spots, save_bookings
from utils import input_date, input_int, input_non_empty

SPOTS_FILE = "data/spots.json"
BOOKINGS_FILE = "data/bookings.json"


def show_spots(spots: list[dict]) -> None:
    """Вывести список парковочных мест."""
    if not spots:
        print("Парковочные места не найдены.")
        return

    print("=" * 45)
    for spot in spots:
        covered = "Крытое" if spot.get("covered") else "Открытое"
        print(f"ID: {spot.get('id')}, номер: {spot.get('number')}")
        print(f"Тип: {covered}, цена: {spot.get('daily_rate')} руб.")
        print("-" * 45)
    print("=" * 45)


def show_bookings(bookings: list[dict]) -> None:
    """Вывести список бронирований."""
    if not bookings:
        print("Бронирования не найдены.")
        return

    print("=" * 45)
    for booking in bookings:
        print(f"ID: {booking.get('id')}")
        print(f"Место: {booking.get('spot_id')}")
        print(f"Клиент: {booking.get('client_name')}")
        print(f"Телефон: {booking.get('client_phone')}")
        print(
            f"Авто: {booking.get('car_model')} "
            f"({booking.get('car_license_plate')})"
        )
        print(f"Период: {booking.get('start')} - {booking.get('end')}")
        print(f"Дней: {booking.get('days')}")
        print(f"Стоимость: {booking.get('total_price')} руб.")
        print(f"Статус: {booking.get('status')}")
        print("-" * 45)
    print("=" * 45)


def show_statistics(spots: list[dict], bookings: list[dict]) -> None:
    """Показать статистику проекта."""
    active_count = 0
    active_revenue = 0.0

    for booking in bookings:
        if booking.get("status") == "active":
            active_count += 1
            active_revenue += float(booking.get("total_price", 0))

    print(f"Всего мест: {len(spots)}")
    print(f"Всего бронирований: {len(bookings)}")
    print(f"Активных бронирований: {active_count}")
    print(f"Выручка по активным броням: {active_revenue} руб.")


def check_availability(bookings: list[dict], spots: list[dict]) -> None:
    """Проверить доступность места на период."""
    show_spots(sort_spots_by_price(spots))

    spot_id = input_int("Введите ID места: ")
    if find_spot_by_id(spots, spot_id) is None:
        print("[ОШИБКА] Место не найдено.")
        return

    start = input_date("Дата начала (ГГГГ-ММ-ДД): ")
    end = input_date("Дата окончания (ГГГГ-ММ-ДД): ")

    if start >= end:
        print("[ОШИБКА] Дата начала должна быть раньше даты окончания.")
        return

    available = is_spot_available(bookings, spot_id, start, end)
    print(get_booking_status(available))


def add_booking(bookings: list[dict], spots: list[dict]) -> bool:
    """Добавить бронирование."""
    show_spots(sort_spots_by_price(spots))

    spot_id = input_int("Введите ID места: ")
    spot = find_spot_by_id(spots, spot_id)

    if spot is None:
        print("[ОШИБКА] Место не найдено.")
        return False

    start = input_date("Дата начала (ГГГГ-ММ-ДД): ")
    end = input_date("Дата окончания (ГГГГ-ММ-ДД): ")

    if start >= end:
        print("[ОШИБКА] Дата начала должна быть раньше даты окончания.")
        return False

    client_name = input_non_empty("Клиент: ")
    client_phone = input_non_empty("Телефон: ")
    car_model = input_non_empty("Модель автомобиля: ")
    car_plate = input_non_empty("Госномер: ")

    daily_rate = float(spot.get("daily_rate", 0))

    booking = create_booking(
        bookings,
        spot_id,
        start,
        end,
        client_name,
        client_phone,
        car_model,
        car_plate,
        daily_rate,
    )

    if booking is None:
        print("[ОШИБКА] Бронирование недоступно или период неверен.")
        return False

    print("Статус: [OK] Бронирование подтверждено!")
    print(f"Итоговая стоимость: {booking['total_price']} руб.")
    return True


def cancel_booking_action(bookings: list[dict]) -> bool:
    """Отменить бронирование."""
    show_bookings(bookings)

    booking_id = input_int("Введите ID брони для отмены: ")

    if cancel_booking(bookings, booking_id):
        print("Бронирование отменено.")
        return True

    print("Бронирование не найдено или уже отменено.")
    return False


def print_menu() -> None:
    """Вывести меню приложения."""
    print("=== Система бронирования парковочных мест ===")
    print("1. Показать места")
    print("2. Проверить доступность")
    print("3. Забронировать место")
    print("4. Отменить бронирование")
    print("5. Показать бронирования")
    print("6. Показать статистику")
    print("0. Выход")


def main() -> None:
    """Главный цикл приложения."""
    spots = load_spots(SPOTS_FILE)
    bookings = load_bookings(BOOKINGS_FILE)

    while True:
        print_menu()
        choice = input("Выберите действие: ")

        if choice == "1":
            show_spots(sort_spots_by_price(spots))
        elif choice == "2":
            check_availability(bookings, spots)
        elif choice == "3":
            if add_booking(bookings, spots):
                save_bookings(BOOKINGS_FILE, bookings)
        elif choice == "4":
            if cancel_booking_action(bookings):
                save_bookings(BOOKINGS_FILE, bookings)
        elif choice == "5":
            show_bookings(bookings)
        elif choice == "6":
            show_statistics(spots, bookings)
        elif choice == "0":
            break
        else:
            print("Неизвестное действие.")


if __name__ == "__main__":
    main()
