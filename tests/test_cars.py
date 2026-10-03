import pytest

from cars import (
    filter_cars_by_price,
    find_car,
    register_car,
    sort_cars,
)


def make_cars() -> list[dict]:
    cars: list[dict] = []
    register_car(cars, "Toyota", "Camry", "А123ВС777", "Иван", 500)
    register_car(cars, "Kia", "Rio", "В456ОР199", "Анна", 350)
    register_car(cars, "Hyundai", "Solaris", "Е789КХ777", "Иван", 300)
    return cars


def test_register_car():
    cars: list[dict] = []
    car = register_car(cars, "Kia", "Rio", "В456ОР199", "Анна", 350)
    assert len(cars) == 1
    assert car["id"] == 1
    assert car["is_available"] is True


def test_register_car_empty_brand():
    with pytest.raises(ValueError):
        register_car([], "", "Rio", "В456ОР199", "Анна", 350)


def test_register_car_duplicate_number():
    cars = make_cars()
    with pytest.raises(ValueError):
        register_car(cars, "Lada", "Vesta", "а123вс777", "Олег", 250)


def test_find_car():
    assert len(find_car(make_cars(), "kia")) == 1
    assert find_car(make_cars(), "bmw") == []


def test_filter_cars_by_price():
    result = filter_cars_by_price(make_cars(), 350)
    assert [car["model"] for car in result] == ["Rio", "Solaris"]


def test_sort_cars():
    prices = [car["price_per_hour"] for car in sort_cars(make_cars())]
    assert prices == [300, 350, 500]
