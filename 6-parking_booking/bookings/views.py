"""Views for bookings."""
from django.shortcuts import render

from models.bookings import find_booking_by_id
from storage import load_bookings, load_spots, load_users

SPOTS_FILE = "data/spots.json"
USERS_FILE = "data/users.json"
BOOKINGS_FILE = "data/bookings.json"


def booking_list(request):
    """Вернуть страницу со списком бронирований."""
    spots_list = load_spots(SPOTS_FILE)
    users_list = load_users(USERS_FILE)
    bookings_list = load_bookings(
        BOOKINGS_FILE,
        spots_list,
        users_list,
    )

    context = {"bookings": bookings_list}
    return render(request, "bookings/booking_list.html", context)


def booking_detail(request, booking_id):
    """Вернуть страницу бронирования."""
    spots_list = load_spots(SPOTS_FILE)
    users_list = load_users(USERS_FILE)
    bookings_list = load_bookings(
        BOOKINGS_FILE,
        spots_list,
        users_list,
    )

    booking = find_booking_by_id(bookings_list, booking_id)

    context = {"booking": booking}
    status = 404 if booking is None else 200

    return render(
        request,
        "bookings/booking_detail.html",
        context,
        status=status,
    )
