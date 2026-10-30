from models import User
from models.users import find_user_by_id


def test_user_creation():
    u = User(1, "Иван", "+7 999 000 00 00")
    assert u.id == 1
    assert u.name == "Иван"


def test_find_user_by_id():
    users = [User(1, "Иван", "+7 999 000 00 00")]
    assert find_user_by_id(users, 1) is not None
    assert find_user_by_id(users, 99) is None
