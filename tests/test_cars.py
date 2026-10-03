import pytest

from models import Car, User
from models.cars import (
    filter_cars_by_price,
    find_car,
    find_car_by_id,
    register_car,
    sort_cars,
)


def make_owner() -> User:
    return User(1, "Иван Петров", "ivan@example.com")


def make_cars() -> list[Car]:
    owner = make_owner()
    cars: list[Car] = []
    register_car(cars, "Toyota", "Camry", "А123ВС777", owner, 500)
    register_car(cars, "Kia", "Rio", "В456ОР199", owner, 350)
    register_car(cars, "Hyundai", "Solaris", "Е789КХ777", owner, 300)
    return cars


def test_car_creation():
    owner = make_owner()
    car = Car(1, "Kia", "Rio", "В456ОР199", owner, 350)
    assert car.id == 1
    assert car.full_name == "Kia Rio"
    assert car.owner is owner
    assert car.is_available is True


def test_car_str():
    car = Car(1, "Kia", "Rio", "В456ОР199", make_owner(), 350)
    text = str(car)
    assert "Kia Rio" in text
    assert "Иван Петров" in text
    assert "350" in text


def test_car_calculate_price_with_discounts():
    car = Car(1, "Kia", "Rio", "В456ОР199", make_owner(), 100)
    assert car.calculate_price(5) == 500
    assert car.calculate_price(6) == 570
    assert car.calculate_price(24) == 2040


def test_car_static_methods():
    assert Car.get_discount_percent(3) == 0
    assert Car.get_discount_percent(10) == 5
    assert Car.get_discount_percent(48) == 15
    assert Car.validate_price(100)
    assert not Car.validate_price(0)


def test_register_car_adds_object():
    cars: list[Car] = []
    car = register_car(cars, "Kia", "Rio", "В456ОР199", make_owner(), 350)
    assert cars == [car]
    assert car.id == 1


def test_register_car_invalid_data():
    owner = make_owner()
    with pytest.raises(ValueError):
        register_car([], "", "Rio", "В456ОР199", owner, 350)
    with pytest.raises(ValueError):
        register_car([], "Kia", "Rio", "В456ОР199", owner, 0)


def test_register_car_duplicate_number():
    cars = make_cars()
    with pytest.raises(ValueError):
        register_car(cars, "Lada", "Vesta", "а123вс777", make_owner(), 250)


def test_find_car_and_find_by_id():
    cars = make_cars()
    assert [car.model for car in find_car(cars, "kia")] == ["Rio"]
    assert find_car(cars, "bmw") == []
    assert find_car_by_id(cars, 2) is cars[1]
    assert find_car_by_id(cars, 99) is None


def test_filter_cars_by_price():
    result = filter_cars_by_price(make_cars(), 350)
    assert [car.model for car in result] == ["Rio", "Solaris"]


def test_sort_cars():
    prices = [car.price_per_hour for car in sort_cars(make_cars())]
    assert prices == [300, 350, 500]
