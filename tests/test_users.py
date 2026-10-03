import pytest

from models import User
from models.users import add_user, find_user, find_user_by_id


def test_user_creation():
    user = User(1, "Иван Петров", "ivan@example.com")
    assert user.id == 1
    assert user.name == "Иван Петров"
    assert user.email == "ivan@example.com"


def test_user_str():
    user = User(1, "Иван Петров", "ivan@example.com")
    assert str(user) == "Иван Петров <ivan@example.com>"


def test_user_from_data():
    user = User.from_data(
        {"id": 2, "name": "Анна Смирнова", "email": "anna@example.com"}
    )
    assert isinstance(user, User)
    assert user.id == 2
    assert user.name == "Анна Смирнова"


def test_validate_email():
    assert User.validate_email("ivan@example.com")
    assert not User.validate_email("ivan.example.com")
    assert not User.validate_email("@example.com")
    assert not User.validate_email("ivan@example")


def test_add_user():
    users: list[User] = []
    first = add_user(users, "Иван Петров", "ivan@example.com")
    second = add_user(users, "Анна Смирнова", "anna@example.com")
    assert users == [first, second]
    assert (first.id, second.id) == (1, 2)


def test_add_user_invalid_data():
    users: list[User] = []
    with pytest.raises(ValueError):
        add_user(users, "", "ivan@example.com")
    with pytest.raises(ValueError):
        add_user(users, "Иван", "not-an-email")
    add_user(users, "Иван", "ivan@example.com")
    with pytest.raises(ValueError):
        add_user(users, "Другой Иван", "IVAN@example.com")


def test_find_user():
    users: list[User] = []
    add_user(users, "Иван Петров", "ivan@example.com")
    add_user(users, "Анна Смирнова", "anna@example.com")
    assert len(find_user(users, "анна")) == 1
    assert len(find_user(users, "example.com")) == 2
    assert find_user_by_id(users, 2) is users[1]
    assert find_user_by_id(users, 5) is None
