"""Класс Trip и функции работы с коллекцией поездок."""
from datetime import date
from typing import Optional

from utils import format_date, next_id

from .cars import Car
from .users import User


class Trip:
    """Поездка: аренда автомобиля пользователем на указанную дату."""

    def __init__(
        self,
        trip_id: int,
        car: Car,
        trip_date: date,
        user: User,
        hours: int,
    ) -> None:
        """Создать объект поездки, связав его с автомобилем и арендатором."""
        self.id = trip_id
        self.car = car
        self.trip_date = trip_date
        self.user = user
        self.hours = hours
        self.is_cancelled = False

    @property
    def price(self) -> int:
        """Стоимость поездки с учётом скидки."""
        return self.car.calculate_price(self.hours)

    def cancel(self) -> None:
        """Отменить поездку (объект остаётся в коллекции)."""
        self.is_cancelled = True

    def __str__(self) -> str:
        """Вернуть строковое представление поездки с учётом состояния."""
        state = "отменена" if self.is_cancelled else "активна"
        return (f"Поездка №{self.id}: {self.car.full_name} "
                f"({self.car.number}), {format_date(self.trip_date)}, "
                f"{self.hours} ч., арендатор: {self.user.name}, "
                f"{self.price} руб. [{state}]")


def check_availability(is_available: bool) -> str:
    """Вернуть текстовый статус доступности автомобиля (функция из ПР1)."""
    if is_available:
        return "Автомобиль доступен для аренды."
    return "Автомобиль занят и недоступен для аренды."


def get_price_description(car: Car, hours: int) -> str:
    """Вернуть текстовое описание стоимости поездки."""
    price = car.calculate_price(hours)
    discount = Car.get_discount_percent(hours)
    if discount == 15:
        return (f"Стоимость поездки: {price} руб. "
                "(применена скидка 15% за аренду от 24 часов).")
    if discount == 5:
        return (f"Стоимость поездки: {price} руб. "
                "(применена скидка 5% за аренду от 6 часов).")
    return f"Стоимость поездки: {price} руб."


def is_car_available(
    trips: list[Trip],
    car: Car,
    trip_date: date,
) -> bool:
    """Проверить, свободен ли автомобиль на дату.

    Активная поездка блокирует автомобиль, отменённая — нет.
    """
    if not car.is_available:
        return False
    return not any(
        trip.car.id == car.id
        and trip.trip_date == trip_date
        and not trip.is_cancelled
        for trip in trips
    )


def create_trip(
    trips: list[Trip],
    car: Car,
    user: User,
    trip_date: date,
    hours: int,
) -> Optional[Trip]:
    """Оформить поездку и добавить её в коллекцию trips.

    Возвращает объект Trip или None, если автомобиль занят.
    Выбрасывает ValueError, если длительность некорректна.
    """
    if hours <= 0:
        raise ValueError("длительность поездки должна быть больше нуля")
    if not is_car_available(trips, car, trip_date):
        return None

    trip = Trip(next_id(item.id for item in trips), car, trip_date,
                user, hours)
    trips.append(trip)
    return trip


def find_trip_by_id(trips: list[Trip], trip_id: int) -> Optional[Trip]:
    """Найти поездку по идентификатору."""
    for trip in trips:
        if trip.id == trip_id:
            return trip
    return None


def cancel_trip(trips: list[Trip], trip_id: int) -> bool:
    """Отменить активную поездку.

    Возвращает False, если поездка не найдена или уже отменена.
    """
    trip = find_trip_by_id(trips, trip_id)
    if trip is None or trip.is_cancelled:
        return False
    trip.cancel()
    return True


def show_trips(trips: list[Trip]) -> None:
    """Вывести список поездок."""
    if not trips:
        print("Список поездок пуст.")
        return
    for trip in trips:
        print(trip)


def display_trip(trip: Trip) -> None:
    """Вывести карточку поездки (функция из ПР1)."""
    discount = Car.get_discount_percent(trip.hours)
    price_text = f"{trip.price} руб."
    if discount:
        price_text += f" (скидка {discount}%)"
    print("   СИСТЕМА КАРШЕРИНГА — КАРТОЧКА ПОЕЗДКИ")
    print(f"ДАТА ПОЕЗДКИ : {format_date(trip.trip_date)}")
    print(f"ПОЛЬЗОВАТЕЛЬ : {trip.user.name}")
    print(f"АВТОМОБИЛЬ   : {trip.car.full_name} ({trip.car.number})")
    print(f"ВЛАДЕЛЕЦ     : {trip.car.owner.name}")
    print(f"ДЛИТЕЛЬНОСТЬ : {trip.hours} ч.")
    print(f"СТОИМОСТЬ    : {price_text}")


def get_statistics(
    cars: list[Car],
    users: list[User],
    trips: list[Trip],
) -> dict:
    """Собрать статистику по автомобилям, пользователям и поездкам."""
    active = [trip for trip in trips if not trip.is_cancelled]
    return {
        "cars": len(cars),
        "available_cars": sum(1 for car in cars if car.is_available),
        "users": len(users),
        "trips": len(trips),
        "active_trips": len(active),
        "cancelled_trips": len(trips) - len(active),
        "revenue": sum(trip.price for trip in active),
    }
