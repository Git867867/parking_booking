"""Тесты класса Spot и функций работы с местами."""

from models import Spot
from models.spots import find_spot_by_id, sort_spots_by_price


def test_spot_creation() -> None:
    spot = Spot(1, "A-15", True, 450.75)
    assert spot.id == 1
    assert spot.number == "A-15"
    assert spot.covered is True
    assert spot.daily_rate == 450.75


def test_spot_str() -> None:
    spot = Spot(1, "A-15", True, 450.75)
    text = str(spot)
    assert "A-15" in text
    assert "450.75" in text


def test_find_spot_by_id() -> None:
    spots = [Spot(1, "A-01", True, 100.0)]
    assert find_spot_by_id(spots, 1) is not None
    assert find_spot_by_id(spots, 99) is None


def test_sort_spots_by_price() -> None:
    spots = [
        Spot(1, "A-01", True, 300.0),
        Spot(2, "A-02", False, 100.0),
    ]
    result = sort_spots_by_price(spots)
    assert result[0].daily_rate == 100.0
    assert result[1].daily_rate == 300.0
