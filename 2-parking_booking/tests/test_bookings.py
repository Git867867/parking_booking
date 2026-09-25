"""Тесты функций бронирования."""

from datetime import date

from bookings import (
    calculate_days,
    cancel_booking,
    create_booking,
    get_booking_status,
    is_spot_available,
)


def test_calculate_days() -> None:
    """Период из пяти дней считается как 5 дней."""
    start = date(2026, 9, 20)
    end = date(2026, 9, 25)
    assert calculate_days(start, end) == 5


def test_get_booking_status() -> None:
    """Статус брони возвращается текстом."""
    assert get_booking_status(True) == "Бронирование доступно"
    assert get_booking_status(False) == "Бронирование недоступно"


def test_create_and_cancel_booking() -> None:
    """Создание брони занимает место, отмена освобождает."""
    bookings = []

    booking = create_booking(
        bookings,
        1,
        date(2026, 9, 20),
        date(2026, 9, 25),
        "Иванов Иван Иванович",
        "+7 999 123-45-67",
        "Kia Rio",
        "Е777ОУ777",
        450.75,
    )

    assert booking is not None
    assert booking["total_price"] == 2253

    assert not is_spot_available(
        bookings, 1, date(2026, 9, 24), date(2026, 9, 26),
    )

    assert cancel_booking(bookings, booking["id"])

    assert is_spot_available(
        bookings, 1, date(2026, 9, 24), date(2026, 9, 26),
    )
