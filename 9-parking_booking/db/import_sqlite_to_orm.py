import os
import sqlite3
import sys
from datetime import date
from pathlib import Path

import django
from django.db import transaction

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

SOURCE_DB = BASE_DIR / "data" / "parking.sqlite"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "parking.settings")
django.setup()

from bookings.models import Booking  # noqa: E402
from spots.models import Spot  # noqa: E402
from users.models import User  # noqa: E402


def main():
    if not SOURCE_DB.exists():
        raise FileNotFoundError(f"Исходная база не найдена: {SOURCE_DB}")

    with sqlite3.connect(SOURCE_DB) as connection:
        connection.row_factory = sqlite3.Row

        spots = connection.execute(
            "SELECT id, number, covered, daily_rate FROM spots ORDER BY id"
        ).fetchall()

        users = connection.execute(
            "SELECT id, name, phone FROM users ORDER BY id"
        ).fetchall()

        bookings = connection.execute(
            """
            SELECT id, spot_id, user_id, start, end, is_cancelled
            FROM bookings
            ORDER BY id
            """
        ).fetchall()

        with transaction.atomic():
            for row in spots:
                Spot.objects.update_or_create(
                    pk=row["id"],
                    defaults={
                        "number": row["number"],
                        "covered": bool(row["covered"]),
                        "daily_rate": row["daily_rate"],
                    },
                )

            for row in users:
                User.objects.update_or_create(
                    pk=row["id"],
                    defaults={
                        "name": row["name"],
                        "phone": row["phone"],
                    },
                )

            for row in bookings:
                Booking.objects.update_or_create(
                    pk=row["id"],
                    defaults={
                        "spot_id": row["spot_id"],
                        "user_id": row["user_id"],
                        "start": date.fromisoformat(row["start"]),
                        "end": date.fromisoformat(row["end"]),
                        "is_cancelled": bool(row["is_cancelled"]),
                    },
                )

    print("Перенос данных завершён.")
    print(f"Мест: {Spot.objects.count()}")
    print(f"Пользователей: {User.objects.count()}")
    print(f"Бронирований: {Booking.objects.count()}")


if __name__ == "__main__":
    main()
