from dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str
    phone: str

    @classmethod
    def from_data(cls, data):
        return cls(id=data["id"], name=data["name"], phone=data["phone"])


def find_user_by_id(users, user_id):
    for u in users:
        if u.id == user_id:
            return u
    return None
