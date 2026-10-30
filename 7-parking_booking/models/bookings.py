from dataclasses import dataclass, field
from datetime import date


@dataclass
class Booking:
    booking_id: int
    spot: object
    user: object
    start: date
    end: date
    is_cancelled: bool = field(default=False)

    def __init__(self, booking_id, spot, user, start, end, is_cancelled=False):
        self.id = booking_id
        self.spot = spot
        self.user = user
        self.start = start
        self.end = end
        self.is_cancelled = bool(is_cancelled)

    def days(self):
        if self.end < self.start:
            return 0
        return (self.end - self.start).days

    def total_price(self):
        return self.days() * self.spot.daily_rate

    def cancel(self):
        self.is_cancelled = True


def create_booking(bookings, spot, user, start, end):
    if end < start:
        return None
    new_id = max([b.id for b in bookings], default=0) + 1
    b = Booking(new_id, spot, user, start, end)
    bookings.append(b)
    return b


def cancel_booking(bookings, booking_id):
    for b in bookings:
        if b.id == booking_id:
            b.cancel()
            return True
    return False


def find_booking_by_id(bookings, booking_id):
    for b in bookings:
        if b.id == booking_id:
            return b
    return None


def is_spot_available(bookings, spot, start, end):
    for b in bookings:
        if b.spot.id == spot.id and not b.is_cancelled:
            if not (end < b.start or start > b.end):
                return False
    return True
