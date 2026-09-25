"""Класс парковочного места и функции работы с местами."""

from typing import Optional


class Spot:
    """Парковочное место."""

    def __init__(
        self,
        spot_id: int,
        number: str,
        covered: bool,
        daily_rate: float,
    ) -> None:
        """Создать объект парковочного места."""
        self.id = spot_id
        self.number = number
        self.covered = covered
        self.daily_rate = daily_rate

    def __str__(self) -> str:
        """Вернуть строковое представление места."""
        covered_text = "Крытое" if self.covered else "Открытое"
        return (
            f"ID: {self.id}, номер: {self.number}, "
            f"тип: {covered_text}, цена: {self.daily_rate} руб."
        )


def find_spot_by_id(
    spots: list[Spot],
    spot_id: int,
) -> Optional[Spot]:
    """Найти место по идентификатору."""
    for spot in spots:
        if spot.id == spot_id:
            return spot
    return None


def sort_spots_by_price(spots: list[Spot]) -> list[Spot]:
    """Отсортировать места по суточной цене."""
    return sorted(spots, key=lambda spot: spot.daily_rate)
