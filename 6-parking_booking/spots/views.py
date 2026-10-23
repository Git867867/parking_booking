"""Views for parking spots."""
from datetime import date, timedelta

from django.shortcuts import render

from models.bookings import is_spot_available
from models.spots import find_spot_by_id
from storage import load_bookings, load_spots, load_users

SPOTS_FILE = "data/spots.json"
USERS_FILE = "data/users.json"
BOOKINGS_FILE = "data/bookings.json"


def spot_list(request):
    """Вернуть страницу со списком парковочных мест."""
    spots_list = load_spots(SPOTS_FILE)
    context = {"spots": spots_list}
    return render(request, "spots/spot_list.html", context)


def spot_detail(request, spot_id):
    """Вернуть страницу парковочного места."""
    spots_list = load_spots(SPOTS_FILE)
    spot = find_spot_by_id(spots_list, spot_id)
    available = False

    if spot is not None:
        users_list = load_users(USERS_FILE)
        bookings_list = load_bookings(
            BOOKINGS_FILE,
            spots_list,
            users_list,
        )
        start = date.today()
        end = start + timedelta(days=1)
        available = is_spot_available(
            bookings_list,
            spot,
            start,
            end,
        )

    context = {"spot": spot, "available": available}
    status = 404 if spot is None else 200

    return render(
        request,
        "spots/spot_detail.html",
        context,
        status=status,
    )
