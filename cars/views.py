"""Страницы автомобилей: view готовит данные ПР3 и вызывает render()."""
from datetime import date

from django.shortcuts import render

from models import Car
from models.cars import find_car_by_id
from models.trips import is_car_available
from storage import load_cars, load_trips, load_users

# Длительности аренды для таблицы цен на странице автомобиля.
PRICE_EXAMPLE_HOURS = (1, 6, 24)


def cars(request):
    """Страница /cars/: список автомобилей."""
    context = {
        "cars": load_cars(load_users()),
    }
    return render(request, "cars/car_list.html", context)


def car_detail(request, car_id):
    """Страница /cars/<id>/: карточка автомобиля (404, если не найден)."""
    users_list = load_users()
    cars_list = load_cars(users_list)
    car = find_car_by_id(cars_list, car_id)

    context = {"car": car}
    if car is not None:
        trips_list = load_trips(cars_list, users_list)
        context["is_free_today"] = is_car_available(
            trips_list, car, date.today()
        )
        context["prices"] = [
            {
                "hours": hours,
                "price": car.calculate_price(hours),
                "discount": Car.get_discount_percent(hours),
            }
            for hours in PRICE_EXAMPLE_HOURS
        ]

    return render(
        request,
        "cars/car_detail.html",
        context,
        status=404 if car is None else 200,
    )
