import os
import sys
from pathlib import Path
from datetime import date, timedelta
from decimal import Decimal

import django

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parking.settings')
django.setup()

from spots.models import Spot
from users.models import User
from bookings.models import Booking

spots_data = [
    ('A1', True, '500.00'), ('A2', True, '550.00'), ('B1', False, '300.00'),
    ('B2', False, '350.00'), ('C1', True, '600.00'), ('C2', False, '400.00'),
]
for n, cov, rate in spots_data:
    Spot.objects.get_or_create(
        number=n,
        defaults={'covered': cov, 'daily_rate': Decimal(rate)}
    )

users_data = [
    ('Иван Иванов', '+79001111111'),
    ('Петр Петров', '+79002222222'),
    ('Анна Сидорова', '+79003333333'),
]
for nm, ph in users_data:
    User.objects.get_or_create(name=nm, defaults={'phone': ph})

spots = list(Spot.objects.all())
users = list(User.objects.all())
today = date.today()

bookings_data = [
    (spots[0], users[0], 0, 2, False), (spots[1], users[1], -1, 1, False),
    (spots[2], users[2], 3, 5, False), (spots[0], users[1], 5, 7, True),
    (spots[3], users[2], 10, 12, False), (spots[4], users[0], -5, -3, True),
]

for s, u, s_off, e_off, canc in bookings_data:
    Booking.objects.get_or_create(
        spot=s,
        user=u,
        start=today + timedelta(days=s_off),
        end=today + timedelta(days=e_off),
        defaults={'is_cancelled': canc}
    )

print(
    f'Spots={Spot.objects.count()}, Users={User.objects.count()}, '
    f'Bookings={Booking.objects.count()}'
)
