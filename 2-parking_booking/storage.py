"""Функции загрузки и сохранения данных проекта."""

import json
import os


def load_data(filename: str, default: list[dict]) -> list[dict]:
    """Загрузить список словарей из JSON-файла."""
    if not os.path.exists(filename):
        return default.copy()

    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError):
        return default.copy()

    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]

    return default.copy()


def save_data(filename: str, data: list[dict]) -> None:
    """Сохранить список словарей в JSON-файл."""
    try:
        directory = os.path.dirname(filename)
        if directory:
            os.makedirs(directory, exist_ok=True)

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except OSError:
        print("[ОШИБКА] Не удалось сохранить файл данных.")


def load_spots(filename: str) -> list[dict]:
    """Загрузить парковочные места."""
    return load_data(filename, [])


def load_bookings(filename: str) -> list[dict]:
    """Загрузить бронирования."""
    return load_data(filename, [])


def save_bookings(filename: str, bookings: list[dict]) -> None:
    """Сохранить бронирования."""
    save_data(filename, bookings)
