"""Тесты функций работы с местами."""
from spots import find_spot_by_id, sort_spots_by_price


def test_find_spot_by_id() -> None:
    spots = [{"id": 1, "number": "A-01", "daily_rate": 100.0}]
    assert find_spot_by_id(spots, 1) is not None
    assert find_spot_by_id(spots, 99) is None


def test_sort_spots_by_price() -> None:
    spots = [
        {"id": 1, "daily_rate": 300.0},
        {"id": 2, "daily_rate": 100.0},
    ]
    result = sort_spots_by_price(spots)
    assert result[0]["daily_rate"] == 100.0
    assert result[1]["daily_rate"] == 300.0
