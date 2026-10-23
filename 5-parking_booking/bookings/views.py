"""Views for bookings."""

from html import escape

from django.http import HttpRequest, HttpResponse

from homepage.views import page
from models.bookings import find_booking_by_id
from storage import load_bookings, load_spots, load_users

SPOTS_FILE = "data/spots.json"
USERS_FILE = "data/users.json"
BOOKINGS_FILE = "data/bookings.json"


def bookings(request: HttpRequest) -> HttpResponse:
    """Вернуть страницу со списком бронирований."""
    spots_list = load_spots(SPOTS_FILE)
    users_list = load_users(USERS_FILE)
    bookings_list = load_bookings(
        BOOKINGS_FILE,
        spots_list,
        users_list,
    )

    items = ""

    for booking in bookings_list:
        status = "отменено" if booking.is_cancelled else "активно"
        badge = "bg-secondary" if booking.is_cancelled else "bg-success"

        spot_number = escape(booking.spot.number)
        user_name = escape(booking.user.name)
        period = f"{booking.start} - {booking.end}"

        items += f"""
<li class="list-group-item d-flex justify-content-between">
<a href="/bookings/{booking.id}/">
{spot_number}, {user_name}, {period}
</a>
<span class="badge {badge}">{escape(status)}</span>
</li>
"""

    if not items:
        items = (
            '<li class="list-group-item">'
            "Бронирования не найдены."
            "</li>"
        )

    content = f"""
<h1>Бронирования</h1>
<ul class="list-group">{items}</ul>
"""

    return HttpResponse(page("Парковка – бронирования", content))


def booking_detail(
    request: HttpRequest,
    booking_id: int,
) -> HttpResponse:
    """Вернуть страницу бронирования."""
    spots_list = load_spots(SPOTS_FILE)
    users_list = load_users(USERS_FILE)
    bookings_list = load_bookings(
        BOOKINGS_FILE,
        spots_list,
        users_list,
    )

    booking = find_booking_by_id(bookings_list, booking_id)

    if booking is None:
        content = """
<h1 class="text-danger">Бронирование не найдено</h1>
<a href="/bookings/" class="btn btn-outline-secondary">
← к списку бронирований
</a>
"""
        return HttpResponse(
            page("Бронирование не найдено", content),
            status=404,
        )

    status = "отменено" if booking.is_cancelled else "активно"
    badge = "bg-secondary" if booking.is_cancelled else "bg-success"

    spot_number = escape(booking.spot.number)
    user_name = escape(booking.user.name)
    total_price = escape(str(booking.total_price()))

    content = f"""
<div class="card">
<div class="card-body">
<h5 class="card-title">Бронирование №{booking.id}</h5>
<p class="card-text">Место: {spot_number}</p>
<p class="card-text">Клиент: {user_name}</p>
<p class="card-text">
Период: {booking.start} – {booking.end}
</p>
<p class="card-text">Дней: {booking.days()}</p>
<p class="card-text">Стоимость: {total_price} руб.</p>
<p class="card-text">
Статус:
<span class="badge {badge}">{escape(status)}</span>
</p>
<a href="/bookings/" class="btn btn-outline-secondary">
← к списку бронирований
</a>
</div>
</div>
"""

    return HttpResponse(
        page(f"Бронирование №{booking.id}", content),
        status=200,
    )
