import json
from datetime import date

import pytest

from models import Car, Trip, User
from storage import (
    StorageError,
    load_cars,
    load_trips,
    load_users,
    save_cars,
    save_trips,
    save_users,
)


def test_load_missing_file_returns_empty(tmp_path):
    assert load_users(tmp_path / "users.json") == []


def test_load_broken_json_raises(tmp_path):
    path = tmp_path / "users.json"
    path.write_text("{not json", encoding="utf-8")
    with pytest.raises(StorageError):
        load_users(path)


def test_round_trip_restores_links(tmp_path):
    owner = User(1, "Иван Петров", "ivan@example.com")
    renter = User(2, "Анна Смирнова", "anna@example.com")
    car = Car(1, "Kia", "Rio", "В456ОР199", owner, 350)
    trip = Trip(1, car, date(2026, 10, 15), renter, 8)
    trip.cancel()

    users_file = tmp_path / "users.json"
    cars_file = tmp_path / "cars.json"
    trips_file = tmp_path / "trips.json"
    save_users([owner, renter], users_file)
    save_cars([car], cars_file)
    save_trips([trip], trips_file)

    users = load_users(users_file)
    cars = load_cars(users, cars_file)
    trips = load_trips(cars, users, trips_file)

    assert cars[0].owner is users[0]
    assert trips[0].car is cars[0]
    assert trips[0].user is users[1]
    assert trips[0].trip_date == date(2026, 10, 15)
    assert trips[0].is_cancelled is True


def test_saved_json_contains_only_ids(tmp_path):
    owner = User(1, "Иван Петров", "ivan@example.com")
    car = Car(1, "Kia", "Rio", "В456ОР199", owner, 350)
    trip = Trip(1, car, date(2026, 10, 15), owner, 2)
    trips_file = tmp_path / "trips.json"
    save_trips([trip], trips_file)
    data = json.loads(trips_file.read_text(encoding="utf-8"))
    assert data[0]["car_id"] == 1
    assert data[0]["user_id"] == 1
    assert data[0]["trip_date"] == "2026-10-15"


def test_load_trip_with_unknown_car_raises(tmp_path):
    trips_file = tmp_path / "trips.json"
    trips_file.write_text(json.dumps([{
        "id": 1, "car_id": 7, "user_id": 1, "trip_date": "2026-10-15",
        "hours": 2, "is_cancelled": False,
    }]), encoding="utf-8")
    user = User(1, "Иван", "ivan@example.com")
    with pytest.raises(StorageError):
        load_trips([], [user], trips_file)
