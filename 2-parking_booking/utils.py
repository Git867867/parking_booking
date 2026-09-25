"""Вспомогательные функции ввода."""

from datetime import date, datetime


def input_int(prompt: str) -> int:
    """Запросить целое число с повтором при ошибке."""
    while True:
        value = input(prompt)
        try:
            return int(value)
        except ValueError:
            print("Введите целое число.")


def input_date(prompt: str) -> date:
    """Запросить дату в формате ГГГГ-ММ-ДД."""
    while True:
        value = input(prompt)
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            print("Введите дату в формате ГГГГ-ММ-ДД.")


def input_non_empty(prompt: str) -> str:
    """Запросить непустую строку."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Введите непустое значение.")
