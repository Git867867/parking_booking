"""Класс пользователя и функции работы с пользователями."""

from typing import Optional


class User:
    """Пользователь системы."""

    def __init__(self, user_id: int, name: str, phone: str) -> None:
        """Создать объект пользователя."""
        self.id = user_id
        self.name = name
        self.phone = phone

    def __str__(self) -> str:
        """Вернуть строковое представление пользователя."""
        return f"ID: {self.id}, {self.name}, тел.: {self.phone}"

    @classmethod
    def from_data(cls, data: dict) -> "User":
        """Создать пользователя из словаря."""
        return cls(
            user_id=data["id"],
            name=data["name"],
            phone=data["phone"],
        )


def find_user_by_id(
    users: list[User],
    user_id: int,
) -> Optional[User]:
    """Найти пользователя по идентификатору."""
    for user in users:
        if user.id == user_id:
            return user
    return None
