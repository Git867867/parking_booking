from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import Avg, Count, F, Max, Q
from django.shortcuts import get_object_or_404, render

from bookings.models import Booking
from spots.models import Spot
from users.models import User


def booking_list(request):
    booking_date = request.GET.get("date", "").strip()
    spot_id = request.GET.get("spot", "").strip()
    user_id = request.GET.get("user", "").strip()
    user_name = request.GET.get("user_name", "").strip()
    spot_number = request.GET.get("spot_number", "").strip()
    q = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "date")
    error = None

    bookings_data = Booking.objects.filter(is_cancelled=False)

    if booking_date:
        try:
            selected_date = datetime.strptime(booking_date, "%Y-%m-%d").date()
        except ValueError:
            error = "Укажите корректную дату."
        else:
            bookings_data = bookings_data.filter(
                start__lte=selected_date,
                end__gte=selected_date,
            )

    if spot_id.isdigit():
        bookings_data = bookings_data.filter(spot_id=int(spot_id))

    if user_id.isdigit():
        bookings_data = bookings_data.filter(user_id=int(user_id))

    if user_name:
        bookings_data = bookings_data.filter(user__name__icontains=user_name)

    if spot_number:
        bookings_data = bookings_data.filter(spot__number__icontains=spot_number)

    if q:
        bookings_data = bookings_data.filter(
            Q(spot__number__icontains=q) | Q(user__name__icontains=q)
        )

    bookings_data = bookings_data.annotate(
        spot_number=F("spot__number"),
        daily_rate=F("spot__daily_rate"),
        user_name=F("user__name"),
    )

    sort_fields = {
        "date": "start",
        "spot": "spot__number",
        "user": "user__name",
    }
    sort_field = sort_fields.get(sort, "start")
    bookings_data = bookings_data.order_by(sort_field, "id")

    bookings_data = bookings_data.values(
        "id",
        "start",
        "end",
        "spot_number",
        "daily_rate",
        "user_name",
    )

    paginator = Paginator(bookings_data, 5)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "bookings": page_obj,
        "page_obj": page_obj,
        "booking_date": booking_date,
        "selected_spot": spot_id,
        "selected_user": user_id,
        "user_name": user_name,
        "spot_number": spot_number,
        "q": q,
        "sort": sort,
        "spots": Spot.objects.order_by("number"),
        "users": User.objects.order_by("name"),
        "error": error,
    }
    return render(request, "bookings/booking_list.html", context)


def booking_detail(request, booking_id):
    booking = get_object_or_404(
        Booking.objects.select_related("spot", "user"),
        pk=booking_id,
    )
    return render(
        request,
        "bookings/booking_detail.html",
        {"booking": booking},
    )


def statistics(request):
    statistics_data = (
        Spot.objects.annotate(
            bookings_count=Count(
                "bookings",
                filter=Q(bookings__is_cancelled=False),
            ),
            spot_number=F("number"),
        )
        .values("spot_number", "bookings_count")
        .order_by("-bookings_count")
    )

    total_bookings = Booking.objects.filter(is_cancelled=False).count()

    rates = Spot.objects.aggregate(
        avg_rate=Avg("daily_rate"),
        max_rate=Max("daily_rate"),
    )

    popular = (
        Spot.objects.annotate(
            bookings_count=Count(
                "bookings",
                filter=Q(bookings__is_cancelled=False),
            ),
            spot_number=F("number"),
        )
        .filter(bookings_count__gt=1)
        .values("spot_number", "bookings_count")
        .order_by("-bookings_count")
    )

    context = {
        "statistics": statistics_data,
        "total_bookings": total_bookings,
        "avg_rate": rates["avg_rate"],
        "max_rate": rates["max_rate"],
        "popular": popular,
    }
    return render(request, "bookings/statistics.html", context)
