from .models import Spot


def spot_context(request):
    return {
        "site_name": "Parking Booking",
        "spots_count": Spot.objects.count(),
    }