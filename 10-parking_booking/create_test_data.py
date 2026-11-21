import os
import sys
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

import django

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "parking.settings")
django.setup()

from django.contrib.auth import get_user_model  # noqa: E402
from django.contrib.auth.models import Group, Permission  # noqa: E402

from bookings.models import Booking  # noqa: E402
from spots.models import Spot  # noqa: E402
from users.models import User  # noqa: E402

spots_data = [
    ("A1", True, "500.00"), ("A2", True, "550.00"), ("B1", False, "300.00"),
    ("B2", False, "350.00"), ("C1", True, "600.00"), ("C2", False, "400.00"),
]
for n, cov, rate in spots_data:
    Spot.objects.get_or_create(number=n, defaults={"covered": cov, "daily_rate": Decimal(rate)})

users_data = [
    ("Иван Иванов", "+79001111111"),
    ("Петр Петров", "+79002222222"),
    ("Анна Сидорова", "+79003333333"),
]
for nm, ph in users_data:
    User.objects.get_or_create(name=nm, defaults={"phone": ph})

spots = list(Spot.objects.order_by("number"))
users = list(User.objects.order_by("name"))
today = date.today()
S = Booking.Status

bookings_data = [
    (spots[0], users[0], 0, 2, S.ACTIVE),
    (spots[1], users[1], -1, 1, S.ACTIVE),
    (spots[2], users[2], 3, 5, S.ACTIVE),
    (spots[0], users[1], 5, 7, S.CANCELLED),
    (spots[3], users[2], 10, 12, S.ACTIVE),
    (spots[4], users[0], -5, -3, S.CANCELLED),
    (spots[5], users[1], 0, 1, S.ACTIVE),
    (spots[2], users[0], -2, 0, S.ACTIVE),
    (spots[3], users[1], 1, 3, S.ACTIVE),
    (spots[4], users[2], 4, 6, S.COMPLETED),
    (spots[5], users[0], -7, -6, S.COMPLETED),
    (spots[1], users[2], 8, 9, S.ACTIVE),
]
# Idempotent: key = (spot, user). Re-run updates the same 12 demo rows.
for s, u, s_off, e_off, st in bookings_data:
    start = today + timedelta(days=s_off)
    end = today + timedelta(days=e_off)
    booking = Booking.objects.filter(spot=s, user=u).order_by("pk").first()
    if booking is None:
        Booking.objects.create(spot=s, user=u, start=start, end=end, status=st)
    else:
        booking.start = start
        booking.end = end
        booking.status = st
        booking.save()

group, _ = Group.objects.get_or_create(name="Parking Operators")
group.permissions.set(
    Permission.objects.filter(
        content_type__app_label="spots",
        codename__in=["view_spot", "add_spot", "change_spot"],
    )
)
AuthUser = get_user_model()
if not AuthUser.objects.filter(username="operator").exists():
    operator = AuthUser.objects.create_user("operator", password="Operator#2026", is_staff=True)
    operator.groups.add(group)

print(f"Spots={Spot.objects.count()}, Users={User.objects.count()}, Bookings={Booking.objects.count()}")
print(
    f"Active={Booking.objects.active().count()}, "
    f"Cancelled={Booking.objects.cancelled().count()}, "
    f"Completed={Booking.objects.completed().count()}"
)