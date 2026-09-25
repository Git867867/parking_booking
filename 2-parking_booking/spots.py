"""Функции работы с парковочными местами."""

from typing import Optional


def find_spot_by_id(
    spots: list[dict],
    spot_id: int,
) -> Optional[dict]:
    """Найти место по идентификатору."""
    for spot in spots:
        if spot.get("id") == spot_id:
            return spot
    return None


def sort_spots_by_price(spots: list[dict]) -> list[dict]:
    """Отсортировать места по суточной цене."""
    return sorted(
        spots,
        key=lambda spot: spot.get("daily_rate", 0),
    )
