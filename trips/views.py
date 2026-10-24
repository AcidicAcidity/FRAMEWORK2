"""Страницы поездок: view готовит данные ПР3 и вызывает render()."""
from django.shortcuts import render

from models.trips import find_trip_by_id
from storage import load_cars, load_trips, load_users


def _load_trips():
    """Загрузить поездки вместе со связанными автомобилями и людьми."""
    users_list = load_users()
    cars_list = load_cars(users_list)
    return load_trips(cars_list, users_list)


def trips(request):
    """Страница /trips/: список поездок."""
    context = {
        "trips": _load_trips(),
    }
    return render(request, "trips/trip_list.html", context)


def trip_detail(request, trip_id):
    """Страница /trips/<id>/: карточка поездки (404, если не найдена)."""
    trip = find_trip_by_id(_load_trips(), trip_id)

    context = {
        "trip": trip,
    }
    return render(
        request,
        "trips/trip_detail.html",
        context,
        status=404 if trip is None else 200,
    )
