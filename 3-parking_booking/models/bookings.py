"""Класс бронирования и функции работы с бронированиями."""

from datetime import date
from typing import Optional

from .spots import Spot
from .users import User


class Booking:
    """Бронирование парковочного места."""

    def __init__(
        self,
        booking_id: int,
        spot: Spot,
        user: User,
        start: date,
        end: date,
    ) -> None:
        """Создать объект бронирования."""
        self.id = booking_id
        self.spot = spot
        self.user = user
        self.start = start
        self.end = end
        self.is_cancelled = False

    def cancel(self) -> None:
        """Отменить бронирование."""
        self.is_cancelled = True

    def days(self) -> int:
        """Количество дней бронирования."""
        return (self.end - self.start).days

    def total_price(self) -> float:
        """Итоговая стоимость бронирования."""
        return self.days() * self.spot.daily_rate

    def __str__(self) -> str:
        """Вернуть строковое представление бронирования."""
        status = "Отменено" if self.is_cancelled else "Активно"
        return (
            f"ID: {self.id}, место: {self.spot.number}, "
            f"клиент: {self.user.name}, "
            f"период: {self.start} - {self.end}, "
            f"стоимость: {self.total_price()} руб., статус: {status}"
        )


def is_spot_available(
    bookings: list[Booking],
    spot: Spot,
    start: date,
    end: date,
) -> bool:
    """Проверить, свободно ли место на период."""
    if end <= start:
        return False

    for booking in bookings:
        if booking.spot.id != spot.id:
            continue
        if booking.is_cancelled:
            continue
        if start < booking.end and end > booking.start:
            return False
    return True


def next_booking_id(bookings: list[Booking]) -> int:
    """Вычислить следующий идентификатор бронирования."""
    ids = (b.id for b in bookings)
    return max(ids, default=0) + 1


def create_booking(
    bookings: list[Booking],
    spot: Spot,
    user: User,
    start: date,
    end: date,
) -> Optional[Booking]:
    """Создать новое бронирование."""
    if not is_spot_available(bookings, spot, start, end):
        return None

    booking = Booking(
        booking_id=next_booking_id(bookings),
        spot=spot,
        user=user,
        start=start,
        end=end,
    )
    bookings.append(booking)
    return booking


def cancel_booking(bookings: list[Booking], booking_id: int) -> bool:
    """Отменить бронирование по ID."""
    for booking in bookings:
        if booking.id != booking_id:
            continue
        if booking.is_cancelled:
            return False
        booking.cancel()
        return True
    return False


def get_booking_status(is_available: bool) -> str:
    """Вернуть текстовый статус места."""
    if is_available:
        return "Место доступно для бронирования"
    return "Место уже занято"
