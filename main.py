"""Система совместного использования автомобилей (каршеринг).

Консольное приложение: точка запуска и пользовательские сценарии.
Данные приложения — коллекции объектов Car, User и Trip.
"""

from typing import Optional
import sys
from models import Car, User, Trip
from models.cars import (
    filter_cars_by_price,
    find_car,
    find_car_by_id,
    register_car,
    show_cars,
    sort_cars,
)
from models.trips import (
    cancel_trip,
    check_availability,
    create_trip,
    display_trip,
    get_price_description,
    get_statistics,
    is_car_available,
    show_trips,
)
from models.users import (
    add_user,
    find_user,
    find_user_by_id,
    show_users,
)
from storage import (
    StorageError,
    load_cars,
    load_trips,
    load_users,
    save_cars,
    save_trips,
    save_users,
)
from utils import input_date, input_int, input_str

MENU = """
=== Система совместного использования автомобилей ===

1. Показать автомобили
2. Найти автомобиль
3. Автомобили до заданной цены
4. Автомобили по возрастанию цены
5. Зарегистрировать автомобиль
6. Проверить доступность на дату
7. Рассчитать стоимость поездки
8. Оформить поездку
9. Отменить поездку
10. Показать поездки
11. Показать пользователей
12. Добавить пользователя
13. Найти пользователя
14. Статистика
0. Выход
"""


def ask_car(cars: list[Car]) -> Optional[Car]:
    """Запросить ID автомобиля и вернуть найденный объект Car."""
    car_id = input_int("ID автомобиля: ")
    car = find_car_by_id(cars, car_id)
    if car is None:
        print(f"Ошибка: автомобиль с ID {car_id} не найден.")
    return car


def ask_user(users: list[User], prompt: str) -> Optional[User]:
    """Запросить ID пользователя и вернуть найденный объект User."""
    user_id = input_int(prompt)
    user = find_user_by_id(users, user_id)
    if user is None:
        print(f"Ошибка: пользователь с ID {user_id} не найден.")
    return user


def search_cars(cars: list[Car]) -> None:
    """Сценарий: поиск автомобиля по подстроке."""
    show_cars(find_car(cars, input_str("Марка, модель или номер: ")))


def show_cars_up_to_price(cars: list[Car]) -> None:
    """Сценарий: отбор автомобилей по предельной цене."""
    max_price = input_int("Максимальная цена за час, руб.: ", 1)
    show_cars(filter_cars_by_price(cars, max_price))


def register_new_car(cars: list[Car], users: list[User]) -> None:
    """Сценарий: регистрация автомобиля владельцем."""
    show_users(users)
    owner = ask_user(users, "ID владельца: ")
    if owner is None:
        return
    brand = input_str("Марка: ")
    model = input_str("Модель: ")
    number = input_str("Государственный номер: ")
    price = input_int("Стоимость аренды за 1 час, руб.: ", 1)
    try:
        car = register_car(cars, brand, model, number, owner, price)
    except ValueError as error:
        print(f"Ошибка: {error}.")
        return
    print(f"Автомобиль {car.full_name} ({car.number}) "
          f"зарегистрирован владельцем {car.owner.name}.")


def check_car_on_date(cars: list[Car], trips: list[Trip]) -> None:
    """Сценарий: проверка доступности автомобиля на дату."""
    car = ask_car(cars)
    if car is None:
        return
    trip_date = input_date("Дата (ДД.ММ.ГГГГ): ")
    print(check_availability(is_car_available(trips, car, trip_date)))


def show_price(cars: list[Car]) -> None:
    """Сценарий: расчёт стоимости поездки."""
    car = ask_car(cars)
    if car is None:
        return
    hours = input_int("Длительность, ч: ", 1)
    print(get_price_description(car, hours))


def create_new_trip(
    trips: list[Trip],
    cars: list[Car],
    users: list[User],
) -> None:
    """Сценарий: оформление поездки.

    Находит объекты Car и User, проверяет доступность и вызывает
    create_trip(), который создаёт объект Trip.
    """
    car = ask_car(cars)
    if car is None:
        return
    user = ask_user(users, "ID пользователя (арендатора): ")
    if user is None:
        return
    trip_date = input_date("Дата поездки (ДД.ММ.ГГГГ): ")
    hours = input_int("Длительность, ч: ", 1)
    try:
        trip = create_trip(trips, car, user, trip_date, hours)
    except ValueError as error:
        print(f"Ошибка: {error}.")
        return
    if trip is None:
        print(check_availability(False))
        return
    print(f"Поездка №{trip.id} оформлена.\n")
    display_trip(trip)


def cancel_existing_trip(trips: list[Trip]) -> None:
    """Сценарий: отмена поездки."""
    trip_id = input_int("ID поездки: ")
    if cancel_trip(trips, trip_id):
        print(f"Поездка №{trip_id} отменена.")
    else:
        print(f"Ошибка: активная поездка №{trip_id} не найдена.")


def add_new_user(users: list[User]) -> None:
    """Сценарий: добавление пользователя."""
    name = input_str("Имя: ")
    email = input_str("Электронная почта: ")
    try:
        user = add_user(users, name, email)
    except ValueError as error:
        print(f"Ошибка: {error}.")
        return
    print(f"Пользователь добавлен: {user.id}. {user}")


def search_users(users: list[User]) -> None:
    """Сценарий: поиск пользователя по имени или почте."""
    found = find_user(users, input_str("Имя или почта: "))
    show_users(found)


def show_stats(
    cars: list[Car],
    users: list[User],
    trips: list[Trip],
) -> None:
    """Сценарий: вывод статистики."""
    stats = get_statistics(cars, users, trips)
    print(f"Автомобилей: {stats['cars']} "
          f"(доступно: {stats['available_cars']})")
    print(f"Пользователей: {stats['users']}")
    print(f"Поездок: {stats['trips']} "
          f"(активных: {stats['active_trips']}, "
          f"отменённых: {stats['cancelled_trips']})")
    print(f"Выручка по активным поездкам: {stats['revenue']} руб.")


def main() -> None:
    """Точка запуска приложения: загрузка данных и цикл меню."""
    try:
        users = load_users()
        cars = load_cars(users)
        trips = load_trips(cars, users)
    except StorageError as error:
        print(f"Ошибка данных: {error}.")
        sys.exit(1)

    actions = {
        "1": lambda: show_cars(cars),
        "2": lambda: search_cars(cars),
        "3": lambda: show_cars_up_to_price(cars),
        "4": lambda: show_cars(sort_cars(cars)),
        "5": lambda: register_new_car(cars, users),
        "6": lambda: check_car_on_date(cars, trips),
        "7": lambda: show_price(cars),
        "8": lambda: create_new_trip(trips, cars, users),
        "9": lambda: cancel_existing_trip(trips),
        "10": lambda: show_trips(trips),
        "11": lambda: show_users(users),
        "12": lambda: add_new_user(users),
        "13": lambda: search_users(users),
        "14": lambda: show_stats(cars, users, trips),
    }

    try:
        while True:
            print(MENU)
            choice = input("Выберите действие: ").strip()
            if choice == "0":
                break
            action = actions.get(choice)
            if action is None:
                print("Ошибка: нет такого пункта меню.")
                continue
            action()
    except (KeyboardInterrupt, EOFError):
        print("\nЗавершение работы.")

    try:
        save_users(users)
        save_cars(cars)
        save_trips(trips)
    except StorageError as error:
        print(f"Ошибка сохранения: {error}.")
        sys.exit(1)
    print("Данные сохранены. До свидания!")


if __name__ == "__main__":
    main()
