from dataclasses import dataclass


@dataclass
class Spot:
    spot_id: int
    number: str
    covered: bool
    daily_rate: float

    def __init__(self, spot_id, number, covered, daily_rate):
        self.id = spot_id
        self.number = str(number)
        self.covered = bool(covered)
        self.daily_rate = float(daily_rate)

    def __str__(self):
        return f"Место {self.number} ({self.daily_rate} руб.)"


def find_spot_by_id(spots, spot_id):
    for s in spots:
        if s.id == spot_id:
            return s
    return None


def sort_spots_by_price(spots):
    return sorted(spots, key=lambda s: s.daily_rate)
