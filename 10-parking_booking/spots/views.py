from datetime import date, datetime

from django.shortcuts import get_object_or_404, render

from bookings.models import Booking
from spots.models import Spot


def spot_list(request):
    covered = request.GET.get("covered", "").strip()
    search = request.GET.get("search", "").strip()
    sort = request.GET.get("sort", "").strip()
    direction = request.GET.get("direction", "asc").strip()

    spots_list = Spot.objects.all()
    if covered == "1":
        spots_list = spots_list.filter(covered=True)
    elif covered == "0":
        spots_list = spots_list.filter(covered=False)
    if search:
        spots_list = spots_list.filter(number__icontains=search)

    allowed_sort_fields = {"number": "number", "rate": "daily_rate"}
    if sort in allowed_sort_fields:
        sort_field = allowed_sort_fields[sort]
        if direction == "desc":
            sort_field = f"-{sort_field}"
        spots_list = spots_list.order_by(sort_field, "id")
    elif covered in ("0", "1"):
        spots_list = spots_list.order_by("daily_rate")
    else:
        spots_list = spots_list.order_by("number")

    return render(request, "spots/spot_list.html", {
        "spots": spots_list, "covered": covered, "search": search,
        "sort": sort, "direction": direction,
    })


def spot_detail(request, slug):
    spot = get_object_or_404(Spot, slug=slug)
    today = date.today()
    is_booked = Booking.objects.active().for_date(today).filter(spot=spot).exists()
    return render(request, "spots/spot_detail.html", {"spot": spot, "available": not is_booked})


def available_spots(request):
    booking_date = request.GET.get("date", "").strip()
    spots_list = []
    error = None

    if booking_date:
        try:
            selected_date = datetime.strptime(booking_date, "%Y-%m-%d").date()
        except ValueError:
            error = "Укажите корректную дату."
        else:
            booked_spot_ids = (
                Booking.objects.active().for_date(selected_date).values_list("spot_id", flat=True)
            )
            spots_list = Spot.objects.exclude(pk__in=booked_spot_ids).order_by("number")

    return render(request, "spots/available.html", {
        "spots": spots_list, "booking_date": booking_date, "error": error,
    })