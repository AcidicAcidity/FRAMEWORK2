"""Класс Car и функции работы с коллекцией автомобилей."""
from typing import Iterator, Optional

from utils import next_id

from .users import User


class Car:
    """Автомобиль, который владелец сдаёт в аренду."""

    def __init__(
        self,
        car_id: int,
        brand: str,
        model: str,
        number: str,
        owner: User,
        price_per_hour: int,
        is_available: bool = True,
    ) -> None:
        """Создать объект автомобиля."""
        self.id = car_id
        self.brand = brand
        self.model = model
        self.number = number
        self.owner = owner
        self.price_per_hour = price_per_hour
        self.is_available = is_available

    @property
    def full_name(self) -> str:
        """Марка и модель автомобиля."""
        return f"{self.brand} {self.model}"

    @staticmethod
    def get_discount_percent(hours: int) -> int:
        """Вернуть скидку в процентах за длительную аренду."""
        if hours >= 24:
            return 15
        if hours >= 6:
            return 5
        return 0

    @staticmethod
    def validate_price(price_per_hour: int) -> bool:
        """Проверить корректность стоимости аренды за час."""
        return price_per_hour > 0

    def calculate_price(self, hours: int) -> int:
        """Рассчитать стоимость аренды на hours часов со скидкой."""
        total = hours * self.price_per_hour
        return total * (100 - self.get_discount_percent(hours)) // 100

    def __str__(self) -> str:
        """Вернуть строковое представление автомобиля."""
        status = "доступен" if self.is_available else "недоступен"
        return (f"{self.full_name} ({self.number}), "
                f"{self.price_per_hour} руб./ч, "
                f"владелец: {self.owner.name} [{status}]")


def register_car(
    cars: list[Car],
    brand: str,
    model: str,
    number: str,
    owner: User,
    price_per_hour: int,
) -> Car:
    """Проверить данные автомобиля и зарегистрировать его в коллекции cars.

    Возвращает созданный объект Car.
    Выбрасывает ValueError, если данные некорректны.
    """
    brand, model, number = (
        value.strip() for value in (brand, model, number)
    )
    if not brand:
        raise ValueError("не указана марка автомобиля")
    if not model:
        raise ValueError("не указана модель автомобиля")
    if not number:
        raise ValueError("не указан государственный номер")
    if not Car.validate_price(price_per_hour):
        raise ValueError("стоимость аренды за час должна быть больше нуля")
    if any(car.number.lower() == number.lower() for car in cars):
        raise ValueError("автомобиль с таким номером уже зарегистрирован")

    car = Car(
        next_id(item.id for item in cars),
        brand,
        model,
        number,
        owner,
        price_per_hour,
    )
    cars.append(car)
    return car


def find_car_by_id(cars: list[Car], car_id: int) -> Optional[Car]:
    """Найти автомобиль по идентификатору."""
    for car in cars:
        if car.id == car_id:
            return car
    return None


def find_car(cars: list[Car], query: str) -> list[Car]:
    """Найти автомобили по подстроке марки, модели или номера."""
    query = query.strip().lower()
    return [
        car for car in cars
        if query in f"{car.full_name} {car.number}".lower()
    ]


def _iter_cars_up_to_price(
    cars: list[Car],
    max_price: int,
) -> Iterator[Car]:
    """Генератор: выдаёт автомобили не дороже max_price за час."""
    for car in cars:
        if car.price_per_hour <= max_price:
            yield car


def filter_cars_by_price(cars: list[Car], max_price: int) -> list[Car]:
    """Отобрать автомобили со стоимостью аренды не выше max_price."""
    return list(_iter_cars_up_to_price(cars, max_price))


def sort_cars(cars: list[Car]) -> list[Car]:
    """Вернуть автомобили, упорядоченные по стоимости аренды за час."""
    return sorted(cars, key=lambda car: car.price_per_hour)


def show_cars(cars: list[Car]) -> None:
    """Вывести список автомобилей."""
    if not cars:
        print("Список автомобилей пуст.")
        return
    for car in cars:
        print(f"{car.id}. {car}")
