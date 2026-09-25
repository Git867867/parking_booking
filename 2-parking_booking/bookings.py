"""Функции работы с бронированиями."""

from datetime import date
from typing import Optional


def get_booking_status(is_available: bool) -> str:
    """Вернуть текстовый статус бронирования."""
    if is_available:
        return "Бронирование доступно"
    return "Бронирование недоступно"


def calculate_days(start: date, end: date) -> int:
    """Посчитать количество дней бронирования."""
    return (end - start).days


def is_spot_available(
    bookings: list[dict],
    spot_id: int,
    start: date,
    end: date,
) -> bool:
    """Проверить, свободно ли место на период."""
    if end <= start:
        return False

    for booking in bookings:
        if booking.get("spot_id") != spot_id:
            continue

        if booking.get("status") != "active":
            continue

        start_text = booking.get("start", "")
        end_text = booking.get("end", "")

        try:
            booking_start = date.fromisoformat(start_text)
            booking_end = date.fromisoformat(end_text)
        except ValueError:
            continue

        if start < booking_end and end > booking_start:
            return False

    return True


def next_booking_id(bookings: list[dict]) -> int:
    """Вычислить следующий идентификатор бронирования."""
    ids = (booking.get("id", 0) for booking in bookings)
    return max(ids, default=0) + 1


def create_booking(
    bookings: list[dict],
    spot_id: int,
    start: date,
    end: date,
    client_name: str,
    client_phone: str,
    car_model: str,
    car_license_plate: str,
    daily_rate: float,
) -> Optional[dict]:
    """Создать бронирование, если место свободно."""
    days = calculate_days(start, end)

    if days <= 0:
        return None

    if not is_spot_available(bookings, spot_id, start, end):
        return None

    booking = {
        "id": next_booking_id(bookings),
        "spot_id": spot_id,
        "client_name": client_name,
        "client_phone": client_phone,
        "car_model": car_model,
        "car_license_plate": car_license_plate,
        "start": start.isoformat(),
        "end": end.isoformat(),
        "days": days,
        "total_price": int(days * daily_rate),
        "status": "active",
    }

    bookings.append(booking)
    return booking


def cancel_booking(bookings: list[dict], booking_id: int) -> bool:
    """Отменить активное бронирование."""
    for booking in bookings:
        if booking.get("id") != booking_id:
            continue

        if booking.get("status") != "active":
            return False

        booking["status"] = "canceled"
        return True

    return False
