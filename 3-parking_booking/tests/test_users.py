"""Тесты класса User."""

from models import User
from models.users import find_user_by_id


def test_user_creation() -> None:
    user = User(1, "Иван Петров", "+7 999 123-45-67")
    assert user.id == 1
    assert user.name == "Иван Петров"
    assert user.phone == "+7 999 123-45-67"


def test_user_str() -> None:
    user = User(1, "Иван Петров", "+7 999 123-45-67")
    assert "Иван Петров" in str(user)


def test_user_from_data() -> None:
    data = {"id": 5, "name": "Анна", "phone": "+7 900 000-00-00"}
    user = User.from_data(data)
    assert user.id == 5
    assert user.name == "Анна"


def test_find_user_by_id() -> None:
    users = [User(1, "Иван", "+7 999")]
    assert find_user_by_id(users, 1) is not None
    assert find_user_by_id(users, 99) is None
