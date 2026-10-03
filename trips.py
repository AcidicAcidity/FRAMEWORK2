"""Функции для работы с поездками (данные хранятся в словарях)."""
from datetime import date
from typing import Optional

from cars import find_car_by_id
from utils import format_date, next_id


def get_discount_percent(hours: int) -> int:
    """Вернуть скидку в процентах за длительную аренду."""
    if hours >= 24:
        return 15
    if hours >= 6:
        return 5
    return 0


def calculate_price(hours: int, price_per_hour: int) -> int:
    """Рассчитать стоимость поездки с учётом скидки за длительность."""
    total = hours * price_per_hour
    return total * (100 - get_discount_percent(hours)) // 100


def get_price_description(hours: int, price_per_hour: int) -> str:
    """Вернуть текстовое описание стоимости поездки."""
    price = calculate_price(hours, price_per_hour)
    discount = get_discount_percent(hours)
    if discount == 15:
        return (f"Стоимость поездки: {price} руб. "
                "(применена скидка 15% за аренду от 24 часов).")
    if discount == 5:
        return (f"Стоимость поездки: {price} руб. "
                "(применена скидка 5% за аренду от 6 часов).")
    return f"Стоимость поездки: {price} руб."


def check_availability(is_available: bool) -> str:
    """Вернуть текстовый статус доступности автомобиля (функция из ПР1)."""
    if is_available:
        return "Автомобиль доступен для аренды."
    return "Автомобиль занят и недоступен для аренды."


def is_car_available(
    cars: list[dict],
    trips: list[dict],
    car_id: int,
    trip_date: date,
) -> bool:
    """Проверить, свободен ли автомобиль на указанную дату."""
    car = find_car_by_id(cars, car_id)
    if car is None or not car["is_available"]:
        return False
    return not any(
        trip["car_id"] == car_id and trip["trip_date"] == trip_date
        for trip in trips
    )


def create_trip(
    cars: list[dict],
    trips: list[dict],
    car_id: int,
    user: str,
    trip_date: date,
    hours: int,
) -> Optional[dict]:
    """Оформить поездку и добавить её в список trips.

    Возвращает словарь поездки или None, если автомобиль занят.
    Выбрасывает ValueError при некорректных данных.
    """
    user = user.strip()
    if hours <= 0:
        raise ValueError("длительность поездки должна быть больше нуля")
    if not user:
        raise ValueError("не указан пользователь")
    if find_car_by_id(cars, car_id) is None:
        raise ValueError(f"автомобиль с ID {car_id} не найден")
    if not is_car_available(cars, trips, car_id, trip_date):
        return None

    trip = {
        "id": next_id(item["id"] for item in trips),
        "car_id": car_id,
        "user": user,
        "trip_date": trip_date,
        "hours": hours,
    }
    trips.append(trip)
    return trip


def cancel_trip(trips: list[dict], trip_id: int) -> bool:
    """Отменить поездку: удалить её из списка. False, если не найдена."""
    for trip in trips:
        if trip["id"] == trip_id:
            trips.remove(trip)
            return True
    return False


def show_trips(cars: list[dict], trips: list[dict]) -> None:
    """Вывести список поездок."""
    if not trips:
        print("Список поездок пуст.")
        return
    for trip in trips:
        car = find_car_by_id(cars, trip["car_id"])
        name = f"{car['brand']} {car['model']}" if car else "неизвестно"
        print(f"№{trip['id']}: {name}, {format_date(trip['trip_date'])}, "
              f"{trip['hours']} ч., арендатор: {trip['user']}")


def display_trip(car: dict, trip: dict) -> None:
    """Вывести карточку поездки (функция из ПР1)."""
    price = calculate_price(trip["hours"], car["price_per_hour"])
    discount = get_discount_percent(trip["hours"])
    price_text = f"{price} руб."
    if discount:
        price_text += f" (скидка {discount}%)"
    print("   СИСТЕМА КАРШЕРИНГА — КАРТОЧКА ПОЕЗДКИ")
    print(f"ДАТА ПОЕЗДКИ : {format_date(trip['trip_date'])}")
    print(f"ПОЛЬЗОВАТЕЛЬ : {trip['user']}")
    print(f"АВТОМОБИЛЬ   : {car['brand']} {car['model']} ({car['number']})")
    print(f"ВЛАДЕЛЕЦ     : {car['owner']}")
    print(f"ДЛИТЕЛЬНОСТЬ : {trip['hours']} ч.")
    print(f"СТОИМОСТЬ    : {price_text}")


def get_statistics(cars: list[dict], trips: list[dict]) -> dict:
    """Собрать статистику: число автомобилей, поездок и выручка."""
    revenue = 0
    for trip in trips:
        car = find_car_by_id(cars, trip["car_id"])
        if car is not None:
            revenue += calculate_price(trip["hours"], car["price_per_hour"])
    return {
        "cars": len(cars),
        "available_cars": sum(1 for car in cars if car["is_available"]),
        "trips": len(trips),
        "revenue": revenue,
    }
