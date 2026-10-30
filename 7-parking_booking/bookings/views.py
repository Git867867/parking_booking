"""Представления для бронирований."""
import sqlite3

from django.shortcuts import render

from db.database import get_connection


def booking_list(request):
    """Вернуть страницу со списком активных бронирований."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    bookings = conn.execute(
        """SELECT b.id,
                  b.start,
                  b.end,
                  b.is_cancelled,
                  s.number AS spot_number,
                  u.name AS user_name
           FROM bookings b
           JOIN spots s ON b.spot_id = s.id
           JOIN users u ON b.user_id = u.id
           WHERE b.is_cancelled = 0
           ORDER BY b.start;"""
    ).fetchall()
    conn.close()
    return render(
        request,
        "bookings/booking_list.html",
        {"bookings": bookings},
    )


def booking_detail(request, booking_id):
    """Вернуть страницу конкретного бронирования."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    booking = conn.execute(
        """SELECT b.id,
                  b.start,
                  b.end,
                  b.is_cancelled,
                  s.number AS spot_number,
                  s.daily_rate,
                  u.name AS user_name
           FROM bookings b
           JOIN spots s ON b.spot_id = s.id
           JOIN users u ON b.user_id = u.id
           WHERE b.id = ?;""",
        [booking_id],
    ).fetchone()
    conn.close()

    status = 200 if booking else 404
    return render(
        request,
        "bookings/booking_detail.html",
        {"booking": booking},
        status=status,
    )


def statistics(request):
    """Вернуть страницу статистики бронирований."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row

    statistics = conn.execute(
        """SELECT s.number AS spot_number,
                  COUNT(b.id) AS bookings_count
           FROM spots s
           LEFT JOIN bookings b
               ON s.id = b.spot_id AND b.is_cancelled = 0
           GROUP BY s.id, s.number
           ORDER BY bookings_count DESC;"""
    ).fetchall()

    total_row = conn.execute(
        "SELECT COUNT(*) AS cnt FROM bookings WHERE is_cancelled = 0;"
    ).fetchone()
    total_bookings = total_row["cnt"]

    avg_row = conn.execute(
        "SELECT AVG(daily_rate) AS avg_rate FROM spots;"
    ).fetchone()
    avg_rate = avg_row["avg_rate"]

    max_row = conn.execute(
        "SELECT MAX(daily_rate) AS max_rate FROM spots;"
    ).fetchone()
    max_rate = max_row["max_rate"]

    popular = conn.execute(
        """SELECT s.number AS spot_number,
                  COUNT(b.id) AS bookings_count
           FROM spots s
           JOIN bookings b ON s.id = b.spot_id
           WHERE b.is_cancelled = 0
           GROUP BY s.id, s.number
           HAVING COUNT(b.id) > 1
           ORDER BY bookings_count DESC;"""
    ).fetchall()

    conn.close()
    context = {
        "statistics": statistics,
        "total_bookings": total_bookings,
        "avg_rate": avg_rate,
        "max_rate": max_rate,
        "popular": popular,
    }
    return render(request, "bookings/statistics.html", context)
