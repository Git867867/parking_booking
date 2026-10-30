"""Скрипт переноса данных из JSON в SQLite."""
import json

from db.database import get_connection

SPOTS_FILE = "data/spots.json"
USERS_FILE = "data/users.json"
BOOKINGS_FILE = "data/bookings.json"


def load_json(filename):
    """Загрузить данные из JSON-файла."""
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def import_spots(conn):
    """Импортировать парковочные места."""
    spots = load_json(SPOTS_FILE)
    conn.executemany(
        """INSERT OR REPLACE INTO spots
           (id, number, covered, daily_rate)
           VALUES (?, ?, ?, ?)""",
        [
            (
                spot["id"],
                spot["number"],
                int(spot["covered"]),
                spot["daily_rate"],
            )
            for spot in spots
        ],
    )


def import_users(conn):
    """Импортировать пользователей."""
    users = load_json(USERS_FILE)
    conn.executemany(
        """INSERT OR REPLACE INTO users
           (id, name, phone)
           VALUES (?, ?, ?)""",
        [
            (
                user["id"],
                user["name"],
                user["phone"],
            )
            for user in users
        ],
    )


def import_bookings(conn):
    """Импортировать бронирования."""
    bookings = load_json(BOOKINGS_FILE)
    conn.executemany(
        """INSERT OR REPLACE INTO bookings
           (id, spot_id, user_id, start, end, is_cancelled)
           VALUES (?, ?, ?, ?, ?, ?)""",
        [
            (
                booking["id"],
                booking["spot_id"],
                booking["user_id"],
                booking["start"],
                booking["end"],
                int(booking["is_cancelled"]),
            )
            for booking in bookings
        ],
    )


def main():
    """Выполнить перенос данных."""
    conn = get_connection()
    try:
        import_spots(conn)
        import_users(conn)
        import_bookings(conn)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
