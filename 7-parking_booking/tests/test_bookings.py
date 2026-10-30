from datetime import date

from models import Booking, Spot, User
from models.bookings import create_booking, is_spot_available


def make_spot():
    return Spot(1, "A-15", True, 450.75)


def make_user():
    return User(1, "Иван", "+7 999 000 00 00")


def test_booking_creation():
    b = Booking(1, make_spot(), make_user(), date(2026, 9, 20), date(2026, 9, 25))
    assert b.id == 1
    assert b.is_cancelled is False


def test_booking_days():
    b = Booking(1, make_spot(), make_user(), date(2026, 9, 20), date(2026, 9, 25))
    assert b.days() == 5


def test_booking_total_price():
    b = Booking(1, make_spot(), make_user(), date(2026, 9, 20), date(2026, 9, 25))
    assert b.total_price() == 5 * 450.75


def test_cancel():
    b = Booking(1, make_spot(), make_user(), date(2026, 9, 20), date(2026, 9, 25))
    b.cancel()
    assert b.is_cancelled is True


def test_create_booking():
    bookings = []
    b = create_booking(
        bookings, make_spot(), make_user(), date(2026, 9, 20), date(2026, 9, 25)
    )
    assert b is not None
    assert len(bookings) == 1


def test_is_spot_available():
    bookings = []
    spot = make_spot()
    user = make_user()
    create_booking(bookings, spot, user, date(2026, 9, 20), date(2026, 9, 25))
    assert not is_spot_available(bookings, spot, date(2026, 9, 22), date(2026, 9, 26))
    assert is_spot_available(bookings, spot, date(2026, 9, 26), date(2026, 9, 28))
