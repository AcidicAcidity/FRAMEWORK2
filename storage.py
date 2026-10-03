"""Сохранение и загрузка данных проекта в JSON-файлах.

JSON хранит только данные и идентификаторы связанных объектов.
Преобразование «JSON <-> объекты Car, User, Trip» выполняется здесь.
"""
import json
from datetime import date
from pathlib import Path

from models import Car, Trip, User
from models.cars import find_car_by_id
from models.users import find_user_by_id

DATA_DIR = Path(__file__).parent / "data"
USERS_FILE = DATA_DIR / "users.json"
CARS_FILE = DATA_DIR / "cars.json"
TRIPS_FILE = DATA_DIR / "trips.json"


class StorageError(Exception):
    """Ошибка чтения или записи файла данных."""


def _read_json(filename: Path) -> list[dict]:
    """Прочитать список записей из JSON-файла.

    Если файла нет, возвращается пустой список.
    """
    try:
        with open(filename, encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as error:
        raise StorageError(
            f"файл {filename.name} повреждён: {error}"
        ) from error
    except OSError as error:
        raise StorageError(
            f"не удалось прочитать {filename.name}: {error}"
        ) from error
    if not isinstance(data, list):
        raise StorageError(f"файл {filename.name} должен содержать список")
    return data


def _write_json(filename: Path, data: list[dict]) -> None:
    """Записать список записей в JSON-файл."""
    try:
        filename.parent.mkdir(parents=True, exist_ok=True)
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except OSError as error:
        raise StorageError(
            f"не удалось записать {filename.name}: {error}"
        ) from error


def load_users(filename: Path = USERS_FILE) -> list[User]:
    """Загрузить пользователей и создать объекты User."""
    try:
        return [User.from_data(item) for item in _read_json(filename)]
    except (KeyError, TypeError) as error:
        raise StorageError(
            f"файл {filename.name} содержит некорректную запись: {error}"
        ) from error


def save_users(users: list[User], filename: Path = USERS_FILE) -> None:
    """Преобразовать объекты User в данные и сохранить их в JSON."""
    _write_json(filename, [
        {"id": user.id, "name": user.name, "email": user.email}
        for user in users
    ])


def load_cars(
    users: list[User],
    filename: Path = CARS_FILE,
) -> list[Car]:
    """Загрузить автомобили; owner_id заменяется объектом User."""
    cars: list[Car] = []
    try:
        for item in _read_json(filename):
            owner = find_user_by_id(users, item["owner_id"])
            if owner is None:
                raise StorageError(
                    f"автомобиль {item['id']}: не найден владелец "
                    f"с ID {item['owner_id']}"
                )
            cars.append(Car(
                car_id=item["id"],
                brand=item["brand"],
                model=item["model"],
                number=item["number"],
                owner=owner,
                price_per_hour=item["price_per_hour"],
                is_available=item["is_available"],
            ))
    except (KeyError, TypeError) as error:
        raise StorageError(
            f"файл {filename.name} содержит некорректную запись: {error}"
        ) from error
    return cars


def save_cars(cars: list[Car], filename: Path = CARS_FILE) -> None:
    """Преобразовать объекты Car в данные (owner -> owner_id) и сохранить."""
    _write_json(filename, [
        {
            "id": car.id,
            "brand": car.brand,
            "model": car.model,
            "number": car.number,
            "owner_id": car.owner.id,
            "price_per_hour": car.price_per_hour,
            "is_available": car.is_available,
        }
        for car in cars
    ])


def load_trips(
    cars: list[Car],
    users: list[User],
    filename: Path = TRIPS_FILE,
) -> list[Trip]:
    """Загрузить поездки; car_id и user_id заменяются объектами."""
    trips: list[Trip] = []
    try:
        for item in _read_json(filename):
            car = find_car_by_id(cars, item["car_id"])
            user = find_user_by_id(users, item["user_id"])
            if car is None or user is None:
                raise StorageError(
                    f"поездка {item['id']}: не найден автомобиль "
                    f"или пользователь"
                )
            trip = Trip(
                trip_id=item["id"],
                car=car,
                trip_date=date.fromisoformat(item["trip_date"]),
                user=user,
                hours=item["hours"],
            )
            trip.is_cancelled = item["is_cancelled"]
            trips.append(trip)
    except (KeyError, TypeError, ValueError) as error:
        raise StorageError(
            f"файл {filename.name} содержит некорректную запись: {error}"
        ) from error
    return trips


def save_trips(trips: list[Trip], filename: Path = TRIPS_FILE) -> None:
    """Преобразовать объекты Trip в данные (car, user -> id) и сохранить."""
    _write_json(filename, [
        {
            "id": trip.id,
            "car_id": trip.car.id,
            "user_id": trip.user.id,
            "trip_date": trip.trip_date.isoformat(),
            "hours": trip.hours,
            "is_cancelled": trip.is_cancelled,
        }
        for trip in trips
    ])
