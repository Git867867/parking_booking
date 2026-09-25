"""Функции загрузки и сохранения данных проекта."""

import json
import os
from datetime import date

from models import Booking, Spot, User
from models.spots import find_spot_by_id
from models.users import find_user_by_id


def load_data(filename: str, default: list) -> list:
    """Загрузить данные из JSON-файла."""
    if not os.path.exists(filename):
        return default.copy()
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError):
        return default.copy()
    if isinstance(data, list):
        return data
    return default.copy()


def save_data(filename: str, data: list) -> None:
    """Сохранить данные в JSON-файл."""
    try:
        directory = os.path.dirname(filename)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except OSError:
        print("[ОШИБКА] Не удалось сохранить файл данных.")


def load_spots(filename: str) -> list[Spot]:
    """Загрузить парковочные места."""
    raw = load_data(filename, [])
    return [
        Spot(
            spot_id=item["id"],
            number=item["number"],
            covered=item["covered"],
            daily_rate=item["daily_rate"],
        )
        for item in raw
        if isinstance(item, dict)
    ]


def save_spots(filename: str, spots: list[Spot]) -> None:
    """Сохранить парковочные места."""
    data = [
        {
            "id": spot.id,
            "number": spot.number,
            "covered": spot.covered,
            "daily_rate": spot.daily_rate,
        }
        for spot in spots
    ]
    save_data(filename, data)


def load_users(filename: str) -> list[User]:
    """Загрузить пользователей."""
    raw = load_data(filename, [])
    return [
        User.from_data(item)
        for item in raw
        if isinstance(item, dict)
    ]


def save_users(filename: str, users: list[User]) -> None:
    """Сохранить пользователей."""
    data = [
        {"id": user.id, "name": user.name, "phone": user.phone}
        for user in users
    ]
    save_data(filename, data)


def load_bookings(
    filename: str,
    spots: list[Spot],
    users: list[User],
) -> list[Booking]:
    """Загрузить бронирования с восстановлением связей."""
    raw = load_data(filename, [])
    bookings: list[Booking] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        spot = find_spot_by_id(spots, item["spot_id"])
        user = find_user_by_id(users, item["user_id"])
        if spot is None or user is None:
            continue
        booking = Booking(
            booking_id=item["id"],
            spot=spot,
            user=user,
            start=date.fromisoformat(item["start"]),
            end=date.fromisoformat(item["end"]),
        )
        booking.is_cancelled = item.get("is_cancelled", False)
        bookings.append(booking)
    return bookings


def save_bookings(filename: str, bookings: list[Booking]) -> None:
    """Сохранить бронирования."""
    data = [
        {
            "id": b.id,
            "spot_id": b.spot.id,
            "user_id": b.user.id,
            "start": b.start.isoformat(),
            "end": b.end.isoformat(),
            "is_cancelled": b.is_cancelled,
        }
        for b in bookings
    ]
    save_data(filename, data)
