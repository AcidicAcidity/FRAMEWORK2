from datetime import date

import pytest

from cars import register_car
from trips import (
    calculate_price,
    cancel_trip,
    create_trip,
    get_statistics,
    is_car_available,
)

TRIP_DATE = date(2026, 10, 15)


def make_cars() -> list[dict]:
    cars: list[dict] = []
    register_car(cars, "Toyota", "Camry", "А123ВС777", "Иван", 500)
    return cars


def test_calculate_price_without_discount():
    assert calculate_price(5, 100) == 500


def test_calculate_price_with_discounts():
    assert calculate_price(6, 100) == 570
    assert calculate_price(24, 100) == 2040


def test_is_car_available_empty_trips():
    assert is_car_available(make_cars(), [], 1, TRIP_DATE)


def test_duplicate_trip_forbidden():
    cars, trips = make_cars(), []
    assert create_trip(cars, trips, 1, "Анна", TRIP_DATE, 3) is not None
    assert create_trip(cars, trips, 1, "Олег", TRIP_DATE, 2) is None
    assert len(trips) == 1


def test_cancel_trip_frees_car():
    cars, trips = make_cars(), []
    trip = create_trip(cars, trips, 1, "Анна", TRIP_DATE, 3)
    assert cancel_trip(trips, trip["id"])
    assert is_car_available(cars, trips, 1, TRIP_DATE)
    assert not cancel_trip(trips, 99)


def test_create_trip_invalid_hours():
    with pytest.raises(ValueError):
        create_trip(make_cars(), [], 1, "Анна", TRIP_DATE, 0)


def test_get_statistics():
    cars, trips = make_cars(), []
    create_trip(cars, trips, 1, "Анна", TRIP_DATE, 10)
    stats = get_statistics(cars, trips)
    assert stats["trips"] == 1
    assert stats["revenue"] == 4750
