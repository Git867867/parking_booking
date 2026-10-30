"""Представления для парковочных мест."""
import sqlite3
from datetime import date

from django.shortcuts import render

from db.database import get_connection


def spot_list(request):
    """Вернуть страницу со списком парковочных мест."""
    covered = request.GET.get("covered")
    conn = get_connection()
    conn.row_factory = sqlite3.Row

    if covered == "1":
        spots = conn.execute(
            """SELECT id, number, covered, daily_rate
               FROM spots
               WHERE covered = 1
               ORDER BY daily_rate;"""
        ).fetchall()
    elif covered == "0":
        spots = conn.execute(
            """SELECT id, number, covered, daily_rate
               FROM spots
               WHERE covered = 0
               ORDER BY daily_rate;"""
        ).fetchall()
    else:
        spots = conn.execute(
            """SELECT id, number, covered, daily_rate
               FROM spots
               ORDER BY number;"""
        ).fetchall()

    conn.close()
    return render(
        request,
        "spots/spot_list.html",
        {"spots": spots, "covered": covered},
    )


def spot_detail(request, spot_id):
    """Вернуть страницу парковочного места."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    spot = conn.execute(
        "SELECT * FROM spots WHERE id = ?;",
        [spot_id],
    ).fetchone()

    available = False
    if spot:
        today = date.today().isoformat()
        booked_row = conn.execute(
            """SELECT COUNT(*) AS cnt
               FROM bookings
               WHERE spot_id = ?
                 AND start <= ?
                 AND end >= ?
                 AND is_cancelled = 0;""",
            [spot_id, today, today],
        ).fetchone()
        available = booked_row["cnt"] == 0

    conn.close()
    status = 200 if spot else 404
    return render(
        request,
        "spots/spot_detail.html",
        {"spot": spot, "available": available},
        status=status,
    )


def available_spots(request):
    """Поиск свободных мест на выбранную дату."""
    booking_date = request.GET.get("date")
    spots = []

    if booking_date:
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        spots = conn.execute(
            """SELECT id, number, covered, daily_rate
               FROM spots
               WHERE id NOT IN (
                   SELECT spot_id
                   FROM bookings
                   WHERE start <= ?
                     AND end >= ?
                     AND is_cancelled = 0
               )
               ORDER BY number;""",
            [booking_date, booking_date],
        ).fetchall()
        conn.close()

    return render(
        request,
        "spots/available.html",
        {"spots": spots, "booking_date": booking_date},
    )
