"""Views for parking spots."""

from datetime import date, timedelta
from html import escape

from django.http import HttpRequest, HttpResponse

from homepage.views import page
from models.bookings import is_spot_available
from models.spots import find_spot_by_id
from storage import load_bookings, load_spots, load_users

SPOTS_FILE = "data/spots.json"
USERS_FILE = "data/users.json"
BOOKINGS_FILE = "data/bookings.json"


def spots(request: HttpRequest) -> HttpResponse:
    """Вернуть страницу со списком парковочных мест."""
    spots_list = load_spots(SPOTS_FILE)
    items = ""

    for spot in spots_list:
        covered = "Крытое" if spot.covered else "Открытое"
        price = escape(str(spot.daily_rate))
        number = escape(spot.number)

        text = f"Место {number} – {escape(covered)}, {price} руб./сутки"

        items += (
            '<li class="list-group-item">'
            f'<a href="/spots/{spot.id}/">{text}</a>'
            "</li>"
        )

    if not items:
        items = '<li class="list-group-item">Места не найдены.</li>'

    content = f"""
<h1>Парковочные места</h1>
<ul class="list-group">{items}</ul>
"""

    return HttpResponse(page("Парковка – места", content))


def spot_detail(request: HttpRequest, spot_id: int) -> HttpResponse:
    """Вернуть страницу парковочного места."""
    spots_list = load_spots(SPOTS_FILE)
    spot = find_spot_by_id(spots_list, spot_id)

    if spot is None:
        content = """
<h1 class="text-danger">Парковочное место не найдено</h1>
<a href="/spots/" class="btn btn-outline-secondary">
← к списку мест
</a>
"""
        return HttpResponse(
            page("Парковочное место не найдено", content),
            status=404,
        )

    users_list = load_users(USERS_FILE)
    bookings_list = load_bookings(
        BOOKINGS_FILE,
        spots_list,
        users_list,
    )

    start = date.today()
    end = start + timedelta(days=1)
    available = is_spot_available(bookings_list, spot, start, end)

    status = "свободно сегодня" if available else "занято сегодня"
    badge = "bg-success" if available else "bg-danger"

    covered = "Крытое" if spot.covered else "Открытое"
    number = escape(spot.number)
    price = escape(str(spot.daily_rate))

    content = f"""
<div class="card">
<div class="card-body">
<h5 class="card-title">Парковочное место {number}</h5>
<p class="card-text"><strong>ID:</strong> {spot.id}</p>
<p class="card-text"><strong>Тип:</strong> {escape(covered)}</p>
<p class="card-text"><strong>Цена:</strong> {price} руб./сутки</p>
<p class="card-text">
Статус на сегодня:
<span class="badge {badge}">{escape(status)}</span>
</p>
<a href="/spots/" class="btn btn-outline-secondary">
← к списку мест
</a>
</div>
</div>
"""

    return HttpResponse(page(spot.number, content), status=200)
