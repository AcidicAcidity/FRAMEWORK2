"""Класс User и функции работы с коллекцией пользователей."""
from typing import Optional

from utils import next_id


class User:
    """Пользователь системы: владелец автомобиля или арендатор."""

    def __init__(self, user_id: int, name: str, email: str) -> None:
        """Создать объект пользователя."""
        self.id = user_id
        self.name = name
        self.email = email

    @classmethod
    def from_data(cls, data: dict) -> "User":
        """Создать пользователя из словаря с данными (например, из JSON)."""
        return cls(
            user_id=data["id"],
            name=data["name"],
            email=data["email"],
        )

    @staticmethod
    def validate_email(email: str) -> bool:
        """Проверить, что адрес электронной почты выглядит корректно."""
        local, _, domain = email.partition("@")
        return bool(local) and "." in domain and " " not in email

    def __str__(self) -> str:
        """Вернуть строковое представление пользователя."""
        return f"{self.name} <{self.email}>"


def add_user(users: list[User], name: str, email: str) -> User:
    """Создать пользователя и добавить его в коллекцию users.

    Возвращает созданный объект User.
    Выбрасывает ValueError, если данные некорректны.
    """
    name, email = name.strip(), email.strip()
    if not name:
        raise ValueError("не указано имя пользователя")
    if not User.validate_email(email):
        raise ValueError("некорректный адрес электронной почты")
    if any(user.email.lower() == email.lower() for user in users):
        raise ValueError("пользователь с такой почтой уже существует")

    user = User(next_id(item.id for item in users), name, email)
    users.append(user)
    return user


def find_user_by_id(users: list[User], user_id: int) -> Optional[User]:
    """Найти пользователя по идентификатору."""
    for user in users:
        if user.id == user_id:
            return user
    return None


def find_user(users: list[User], query: str) -> list[User]:
    """Найти пользователей по подстроке имени или адреса почты."""
    query = query.strip().lower()
    return [
        user for user in users
        if query in user.name.lower() or query in user.email.lower()
    ]


def show_users(users: list[User]) -> None:
    """Вывести список пользователей."""
    if not users:
        print("Список пользователей пуст.")
        return
    for user in users:
        print(f"{user.id}. {user}")
