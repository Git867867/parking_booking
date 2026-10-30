from datetime import date, datetime

from django.shortcuts import get_object_or_404, render

from bookings.models import Booking
from spots.models import Spot


def spot_list(request):
    covered = request.GET.get("covered", "").strip()
    search = request.GET.get("search", "").strip()

    spots_list = Spot.objects.all()

    if covered == "1":
        spots_list = spots_list.filter(covered=True).order_by("daily_rate")
    elif covered == "0":
        spots_list = spots_list.filter(covered=False).order_by("daily_rate")
    else:
        spots_list = spots_list.order_by("number")

    if search:
        spots_list = spots_list.filter(number__icontains=search)

    return render(
        request,
        "spots/spot_list.html",
        {"spots": spots_list, "covered": covered, "search": search},
    )


def spot_detail(request, spot_id):
    spot = get_object_or_404(Spot, pk=spot_id)

    today = date.today()
    is_booked = Booking.objects.filter(
        spot=spot,
        start__lte=today,
        end__gte=today,
        is_cancelled=False,
    ).exists()

    return render(
        request,
        "spots/spot_detail.html",
        {"spot": spot, "available": not is_booked},
    )


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
            booked_spot_ids = Booking.objects.filter(
                start__lte=selected_date,
                end__gte=selected_date,
                is_cancelled=False,
            ).values_list("spot_id", flat=True)

            spots_list = Spot.objects.exclude(
                pk__in=booked_spot_ids,
            ).order_by("number")

    return render(
        request,
        "spots/available.html",
        {"spots": spots_list, "booking_date": booking_date, "error": error},
    )
