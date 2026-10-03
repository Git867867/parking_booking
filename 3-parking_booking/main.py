"""Точка запуска системы бронирования парковочных мест."""

from models import Booking, Spot, User
from models.bookings import (
    cancel_booking,
    create_booking,
    get_booking_status,
    is_spot_available,
)
from models.spots import find_spot_by_id, sort_spots_by_price
from models.users import find_user_by_id
from storage import (
    load_bookings,
    load_spots,
    load_users,
    save_bookings,
    save_spots,
    save_users,
)
from utils import input_date, input_int, input_non_empty

SPOTS_FILE = "data/spots.json"
USERS_FILE = "data/users.json"
BOOKINGS_FILE = "data/bookings.json"


def show_spots(spots: list[Spot]) -> None:
    """Вывести список парковочных мест."""
    if not spots:
        print("Парковочные места не найдены.")
        return
    print("=" * 45)
    for spot in spots:
        print(spot)
        print("-" * 45)
    print("=" * 45)


def show_users(users: list[User]) -> None:
    """Вывести список пользователей."""
    if not users:
        print("Пользователи не найдены.")
        return
    print("=" * 45)
    for user in users:
        print(user)
    print("=" * 45)


def show_bookings(bookings: list[Booking]) -> None:
    """Вывести список бронирований."""
    if not bookings:
        print("Бронирования не найдены.")
        return
    print("=" * 45)
    for booking in bookings:
        print(booking)
        print("-" * 45)
    print("=" * 45)


def show_statistics(
    spots: list[Spot],
    bookings: list[Booking],
) -> None:
    """Показать статистику."""
    active = [b for b in bookings if not b.is_cancelled]
    revenue = sum(b.total_price() for b in active)
    print(f"Всего мест: {len(spots)}")
    print(f"Всего бронирований: {len(bookings)}")
    print(f"Активных бронирований: {len(active)}")
    print(f"Выручка по активным: {revenue} руб.")


def check_availability(
    bookings: list[Booking],
    spots: list[Spot],
) -> None:
    """Проверить доступность места."""
    show_spots(sort_spots_by_price(spots))
    spot_id = input_int("Введите ID места: ")
    spot = find_spot_by_id(spots, spot_id)
    if spot is None:
        print("[ОШИБКА] Место не найдено.")
        return

    start = input_date("Дата начала (ГГГГ-ММ-ДД): ")
    end = input_date("Дата окончания (ГГГГ-ММ-ДД): ")

    if start >= end:
        print("[ОШИБКА] Дата начала должна быть раньше даты окончания.")
        return

    available = is_spot_available(bookings, spot, start, end)
    print(get_booking_status(available))


def add_booking(
    bookings: list[Booking],
    spots: list[Spot],
    users: list[User],
) -> bool:
    """Создать бронирование."""
    show_spots(sort_spots_by_price(spots))
    spot_id = input_int("Введите ID места: ")
    spot = find_spot_by_id(spots, spot_id)
    if spot is None:
        print("[ОШИБКА] Место не найдено.")
        return False

    show_users(users)
    user_id = input_int("Введите ID пользователя: ")
    user = find_user_by_id(users, user_id)
    if user is None:
        print("[ОШИБКА] Пользователь не найден.")
        return False

    start = input_date("Дата начала (ГГГГ-ММ-ДД): ")
    end = input_date("Дата окончания (ГГГГ-ММ-ДД): ")

    if start >= end:
        print("[ОШИБКА] Дата начала должна быть раньше даты окончания.")
        return False

    booking = create_booking(bookings, spot, user, start, end)
    if booking is None:
        print("[ОШИБКА] Место занято или период неверен.")
        return False

    print("Статус: [OK] Бронирование подтверждено!")
    print(f"Стоимость: {booking.total_price()} руб.")
    return True


def cancel_booking_action(bookings: list[Booking]) -> bool:
    """Отменить бронирование."""
    show_bookings(bookings)
    booking_id = input_int("Введите ID брони для отмены: ")
    if cancel_booking(bookings, booking_id):
        print("Бронирование отменено.")
        return True
    print("Бронирование не найдено или уже отменено.")
    return False


def add_user_action(users: list[User]) -> None:
    """Добавить пользователя."""
    name = input_non_empty("Имя: ")
    phone = input_non_empty("Телефон: ")
    new_id = max((u.id for u in users), default=0) + 1
    user = User(user_id=new_id, name=name, phone=phone)
    users.append(user)
    print(f"Пользователь добавлен: {user}")


def print_menu() -> None:
    """Вывести меню приложения."""
    print("=== Система бронирования парковочных мест ===")
    print("1. Показать места")
    print("2. Показать пользователей")
    print("3. Проверить доступность")
    print("4. Забронировать место")
    print("5. Отменить бронирование")
    print("6. Показать бронирования")
    print("7. Показать статистику")
    print("8. Добавить пользователя")
    print("0. Выход")


def main() -> None:
    """Главный цикл приложения."""
    spots = load_spots(SPOTS_FILE)
    users = load_users(USERS_FILE)
    bookings = load_bookings(BOOKINGS_FILE, spots, users)

    while True:
        print_menu()
        choice = input("Выберите действие: ")

        if choice == "1":
            show_spots(sort_spots_by_price(spots))
        elif choice == "2":
            show_users(users)
        elif choice == "3":
            check_availability(bookings, spots)
        elif choice == "4":
            if add_booking(bookings, spots, users):
                save_bookings(BOOKINGS_FILE, bookings)
        elif choice == "5":
            if cancel_booking_action(bookings):
                save_bookings(BOOKINGS_FILE, bookings)
        elif choice == "6":
            show_bookings(bookings)
        elif choice == "7":
            show_statistics(spots, bookings)
        elif choice == "8":
            add_user_action(users)
            save_users(USERS_FILE, users)
        elif choice == "0":
            save_spots(SPOTS_FILE, spots)
            save_users(USERS_FILE, users)
            save_bookings(BOOKINGS_FILE, bookings)
            print("Данные сохранены. До свидания!")
            break
        else:
            print("Неизвестное действие.")


if __name__ == "__main__":
    main()
