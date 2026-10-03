"""Система совместного использования автомобилей (каршеринг).

Консольное приложение: точка запуска и пользовательские сценарии.
"""
import sys

from cars import (
    filter_cars_by_price,
    find_car,
    find_car_by_id,
    register_car,
    show_cars,
    sort_cars,
)
from storage import (
    StorageError,
    load_cars,
    load_trips,
    save_cars,
    save_trips,
)
from trips import (
    cancel_trip,
    check_availability,
    create_trip,
    display_trip,
    get_price_description,
    get_statistics,
    is_car_available,
    show_trips,
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
11. Статистика
0. Выход
"""


def search_cars(cars: list[dict]) -> None:
    """Сценарий: поиск автомобиля по подстроке."""
    found = find_car(cars, input_str("Марка, модель или номер: "))
    show_cars(found)


def show_cars_up_to_price(cars: list[dict]) -> None:
    """Сценарий: отбор автомобилей по предельной цене."""
    max_price = input_int("Максимальная цена за час, руб.: ", 1)
    show_cars(filter_cars_by_price(cars, max_price))


def register_new_car(cars: list[dict]) -> None:
    """Сценарий: регистрация автомобиля владельцем."""
    owner = input_str("Имя владельца: ")
    brand = input_str("Марка: ")
    model = input_str("Модель: ")
    number = input_str("Государственный номер: ")
    price = input_int("Стоимость аренды за 1 час, руб.: ", 1)
    try:
        car = register_car(cars, brand, model, number, owner, price)
    except ValueError as error:
        print(f"Ошибка: {error}.")
        return
    print(f"Автомобиль {car['brand']} {car['model']} ({car['number']}) "
          f"зарегистрирован владельцем {car['owner']}.")


def check_car_on_date(cars: list[dict], trips: list[dict]) -> None:
    """Сценарий: проверка доступности автомобиля на дату."""
    car_id = input_int("ID автомобиля: ")
    trip_date = input_date("Дата (ДД.ММ.ГГГГ): ")
    if find_car_by_id(cars, car_id) is None:
        print(f"Ошибка: автомобиль с ID {car_id} не найден.")
        return
    print(check_availability(is_car_available(cars, trips, car_id,
                                              trip_date)))


def show_price(cars: list[dict]) -> None:
    """Сценарий: расчёт стоимости поездки."""
    car = find_car_by_id(cars, input_int("ID автомобиля: "))
    if car is None:
        print("Ошибка: автомобиль не найден.")
        return
    hours = input_int("Длительность, ч: ", 1)
    print(get_price_description(hours, car["price_per_hour"]))


def create_new_trip(cars: list[dict], trips: list[dict]) -> None:
    """Сценарий: оформление поездки."""
    car_id = input_int("ID автомобиля: ")
    user = input_str("Имя пользователя (арендатора): ")
    trip_date = input_date("Дата поездки (ДД.ММ.ГГГГ): ")
    hours = input_int("Длительность, ч: ", 1)
    try:
        trip = create_trip(cars, trips, car_id, user, trip_date, hours)
    except ValueError as error:
        print(f"Ошибка: {error}.")
        return
    if trip is None:
        print(check_availability(False))
        return
    print("Поездка оформлена.\n")
    display_trip(find_car_by_id(cars, car_id), trip)


def cancel_existing_trip(trips: list[dict]) -> None:
    """Сценарий: отмена поездки."""
    trip_id = input_int("ID поездки: ")
    if cancel_trip(trips, trip_id):
        print(f"Поездка №{trip_id} отменена.")
    else:
        print(f"Ошибка: поездка №{trip_id} не найдена.")


def show_stats(cars: list[dict], trips: list[dict]) -> None:
    """Сценарий: вывод статистики."""
    stats = get_statistics(cars, trips)
    print(f"Автомобилей: {stats['cars']} "
          f"(доступно: {stats['available_cars']})")
    print(f"Поездок: {stats['trips']}")
    print(f"Выручка: {stats['revenue']} руб.")


def main() -> None:
    """Точка запуска приложения: загрузка данных и цикл меню."""
    try:
        cars = load_cars()
        trips = load_trips()
    except StorageError as error:
        print(f"Ошибка данных: {error}.")
        sys.exit(1)

    actions = {
        "1": lambda: show_cars(cars),
        "2": lambda: search_cars(cars),
        "3": lambda: show_cars_up_to_price(cars),
        "4": lambda: show_cars(sort_cars(cars)),
        "5": lambda: register_new_car(cars),
        "6": lambda: check_car_on_date(cars, trips),
        "7": lambda: show_price(cars),
        "8": lambda: create_new_trip(cars, trips),
        "9": lambda: cancel_existing_trip(trips),
        "10": lambda: show_trips(cars, trips),
        "11": lambda: show_stats(cars, trips),
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
        save_cars(cars)
        save_trips(trips)
    except StorageError as error:
        print(f"Ошибка сохранения: {error}.")
        sys.exit(1)
    print("Данные сохранены. До свидания!")


if __name__ == "__main__":
    main()
