import json
import os
from datetime import date

from models.bookings import Booking
from models.spots import Spot, find_spot_by_id
from models.users import User, find_user_by_id


def load_data(filename, default):
    if not os.path.exists(filename):
        return default.copy()
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        return default.copy()
    return data if isinstance(data, list) else default.copy()


def save_data(filename, data):
    try:
        d = os.path.dirname(filename)
        if d:
            os.makedirs(d, exist_ok=True)
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError:
        pass


def load_spots(filename):
    raw = load_data(filename, [])
    spots = []
    for item in raw:
        try:
            spots.append(
                Spot(item["id"], item["number"], item["covered"], item["daily_rate"])
            )
        except (KeyError, TypeError):
            continue
    return spots


def load_users(filename):
    raw = load_data(filename, [])
    users = []
    for item in raw:
        try:
            users.append(User.from_data(item))
        except (KeyError, TypeError):
            continue
    return users


def load_bookings(filename, spots, users):
    raw = load_data(filename, [])
    bookings = []
    for item in raw:
        spot = find_spot_by_id(spots, item.get("spot_id"))
        user = find_user_by_id(users, item.get("user_id"))
        if spot is None or user is None:
            continue
        try:
            b = Booking(
                item["id"],
                spot,
                user,
                date.fromisoformat(item["start"]),
                date.fromisoformat(item["end"]),
            )
            b.is_cancelled = bool(item.get("is_cancelled", False))
            bookings.append(b)
        except (KeyError, TypeError, ValueError):
            continue
    return bookings
