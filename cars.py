"""Функции для работы с автомобилями (данные хранятся в словарях)."""
from typing import Iterator, Optional

from utils import next_id


def register_car(
    cars: list[dict],
    brand: str,
    model: str,
    number: str,
    owner: str,
    price_per_hour: int,
) -> dict:
    """Проверить данные автомобиля и зарегистрировать его в списке cars.

    Возвращает словарь зарегистрированного автомобиля.
    Выбрасывает ValueError, если данные некорректны.
    """
    brand, model, number, owner = (
        value.strip() for value in (brand, model, number, owner)
    )
    if not brand:
        raise ValueError("не указана марка автомобиля")
    if not model:
        raise ValueError("не указана модель автомобиля")
    if not number:
        raise ValueError("не указан государственный номер")
    if not owner:
        raise ValueError("не указан владелец автомобиля")
    if price_per_hour <= 0:
        raise ValueError("стоимость аренды за час должна быть больше нуля")
    if any(car["number"].lower() == number.lower() for car in cars):
        raise ValueError("автомобиль с таким номером уже зарегистрирован")

    car = {
        "id": next_id(item["id"] for item in cars),
        "brand": brand,
        "model": model,
        "number": number,
        "owner": owner,
        "price_per_hour": price_per_hour,
        "is_available": True,
    }
    cars.append(car)
    return car


def find_car_by_id(cars: list[dict], car_id: int) -> Optional[dict]:
    """Найти автомобиль по идентификатору."""
    for car in cars:
        if car["id"] == car_id:
            return car
    return None


def find_car(cars: list[dict], query: str) -> list[dict]:
    """Найти автомобили по подстроке марки, модели или номера."""
    query = query.strip().lower()
    return [
        car for car in cars
        if query in f"{car['brand']} {car['model']} {car['number']}".lower()
    ]


def _iter_cars_up_to_price(
    cars: list[dict],
    max_price: int,
) -> Iterator[dict]:
    """Генератор: выдаёт автомобили не дороже max_price за час."""
    for car in cars:
        if car["price_per_hour"] <= max_price:
            yield car


def filter_cars_by_price(cars: list[dict], max_price: int) -> list[dict]:
    """Отобрать автомобили со стоимостью аренды не выше max_price."""
    return list(_iter_cars_up_to_price(cars, max_price))


def sort_cars(cars: list[dict]) -> list[dict]:
    """Вернуть автомобили, упорядоченные по стоимости аренды за час."""
    return sorted(cars, key=lambda car: car["price_per_hour"])


def show_cars(cars: list[dict]) -> None:
    """Вывести список автомобилей в виде таблицы."""
    if not cars:
        print("Список автомобилей пуст.")
        return
    print(f"{'ID':<4}{'Автомобиль':<24}{'Номер':<12}"
          f"{'Владелец':<18}{'Руб./ч':>7}  Статус")
    for car in cars:
        name = f"{car['brand']} {car['model']}"
        status = "доступен" if car["is_available"] else "недоступен"
        print(f"{car['id']:<4}{name:<24}{car['number']:<12}"
              f"{car['owner']:<18}{car['price_per_hour']:>7}  {status}")
