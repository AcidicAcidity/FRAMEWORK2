from datetime import date

import pytest

from models import Car, Trip, User
from models.trips import (
    cancel_trip,
    create_trip,
    get_statistics,
    is_car_available,
)

TRIP_DATE = date(2026, 10, 15)


def make_objects() -> tuple[Car, User, User]:
    owner = User(1, "Иван Петров", "ivan@example.com")
    renter = User(2, "Анна Смирнова", "anna@example.com")
    other = User(3, "Пётр Сидоров", "petr@example.com")
    car = Car(1, "Toyota", "Camry", "А123ВС777", owner, 500)
    return car, renter, other


def test_trip_creation_links_objects():
    car, renter, _ = make_objects()
    trip = Trip(1, car, TRIP_DATE, renter, 8)
    assert trip.id == 1
    assert trip.car is car
    assert trip.user is renter
    assert trip.hours == 8
    assert trip.is_cancelled is False


def test_trip_price_uses_car_rate():
    car, renter, _ = make_objects()
    assert Trip(1, car, TRIP_DATE, renter, 5).price == 2500
    assert Trip(2, car, TRIP_DATE, renter, 10).price == 4750


def test_trip_cancel_and_str():
    car, renter, _ = make_objects()
    trip = Trip(1, car, TRIP_DATE, renter, 3)
    assert "активна" in str(trip)
    trip.cancel()
    assert trip.is_cancelled
    assert "отменена" in str(trip)
    assert "Анна Смирнова" in str(trip)


def test_is_car_available_without_trips():
    car, _, _ = make_objects()
    assert is_car_available([], car, TRIP_DATE)


def test_unavailable_car_flag_blocks_trip():
    car, renter, _ = make_objects()
    car.is_available = False
    assert create_trip([], car, renter, TRIP_DATE, 3) is None


def test_duplicate_active_trip_forbidden():
    car, renter, other = make_objects()
    trips: list[Trip] = []
    first = create_trip(trips, car, renter, TRIP_DATE, 3)
    second = create_trip(trips, car, other, TRIP_DATE, 2)
    assert first is not None
    assert second is None
    assert len(trips) == 1


def test_cancelled_trip_does_not_block_car():
    car, renter, other = make_objects()
    trips: list[Trip] = []
    first = create_trip(trips, car, renter, TRIP_DATE, 3)
    assert cancel_trip(trips, first.id)
    assert first in trips and first.is_cancelled
    again = create_trip(trips, car, other, TRIP_DATE, 2)
    assert again is not None
    assert len(trips) == 2


def test_cancel_trip_unknown_or_repeated():
    car, renter, _ = make_objects()
    trips: list[Trip] = []
    trip = create_trip(trips, car, renter, TRIP_DATE, 3)
    assert not cancel_trip(trips, 99)
    assert cancel_trip(trips, trip.id)
    assert not cancel_trip(trips, trip.id)


def test_create_trip_invalid_hours():
    car, renter, _ = make_objects()
    with pytest.raises(ValueError):
        create_trip([], car, renter, TRIP_DATE, 0)


def test_get_statistics_ignores_cancelled():
    car, renter, other = make_objects()
    trips: list[Trip] = []
    create_trip(trips, car, renter, TRIP_DATE, 10)
    cancelled = create_trip(trips, car, other, date(2026, 10, 16), 5)
    cancel_trip(trips, cancelled.id)
    stats = get_statistics([car], [renter, other], trips)
    assert stats["trips"] == 2
    assert stats["active_trips"] == 1
    assert stats["cancelled_trips"] == 1
    assert stats["revenue"] == 4750
