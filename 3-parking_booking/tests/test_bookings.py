"""Тесты класса Booking и функций бронирования."""

from datetime import date

from models import Booking, Spot, User
from models.bookings import (
    cancel_booking,
    create_booking,
    get_booking_status,
    is_spot_available,
)


def make_spot() -> Spot:
    """Вспомогательный конструктор места."""
    return Spot(1, "A-15", True, 450.75)


def make_user() -> User:
    """Вспомогательный конструктор пользователя."""
    return User(1, "Иван Иванов", "+7 999 123-45-67")


def test_booking_creation() -> None:
    spot = make_spot()
    user = make_user()
    booking = Booking(
        1, spot, user, date(2026, 9, 20), date(2026, 9, 25),
    )
    assert booking.id == 1
    assert booking.spot is spot
    assert booking.user is user
    assert booking.is_cancelled is False


def test_booking_days() -> None:
    booking = Booking(
        1, make_spot(), make_user(),
        date(2026, 9, 20), date(2026, 9, 25),
    )
    assert booking.days() == 5


def test_booking_total_price() -> None:
    booking = Booking(
        1, make_spot(), make_user(),
        date(2026, 9, 20), date(2026, 9, 25),
    )
    assert booking.total_price() == 5 * 450.75


def test_booking_cancel() -> None:
    booking = Booking(
        1, make_spot(), make_user(),
        date(2026, 9, 20), date(2026, 9, 25),
    )
    booking.cancel()
    assert booking.is_cancelled is True


def test_get_booking_status() -> None:
    assert get_booking_status(True) == "Место доступно для бронирования"
    assert get_booking_status(False) == "Место уже занято"


def test_create_and_cancel_booking() -> None:
    bookings: list[Booking] = []
    spot = make_spot()
    user = make_user()

    booking = create_booking(
        bookings, spot, user, date(2026, 9, 20), date(2026, 9, 25),
    )
    assert booking is not None
    assert len(bookings) == 1

    assert not is_spot_available(
        bookings, spot, date(2026, 9, 24), date(2026, 9, 26),
    )

    assert cancel_booking(bookings, booking.id) is True
    assert booking.is_cancelled is True

    assert is_spot_available(
        bookings, spot, date(2026, 9, 24), date(2026, 9, 26),
    )


def test_create_booking_invalid_period() -> None:
    """Попытка создать бронирование с некорректным периодом должна вернуть None."""
    bookings: list[Booking] = []
    spot = make_spot()
    user = make_user()

    booking = create_booking(
        bookings, spot, user, date(2026, 9, 25), date(2026, 9, 20),
    )
    assert booking is None
    assert len(bookings) == 0
