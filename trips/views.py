"""Страницы поездок: данные берутся из классов и JSON-хранилища ПР3."""
from django.http import HttpResponse
from django.utils.html import escape

from homepage.views import page
from models.trips import find_trip_by_id
from storage import load_cars, load_trips, load_users
from utils import format_date


def trips(request):
    """Страница /trips/: список поездок."""
    users_list = load_users()
    cars_list = load_cars(users_list)
    items = ""
    for trip in load_trips(cars_list, users_list):
        status = "отменена" if trip.is_cancelled else "активна"
        badge = "bg-secondary" if trip.is_cancelled else "bg-success"
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/trips/{trip.id}/">
                {escape(trip.car.full_name)} –
                {format_date(trip.trip_date)}
            </a>
            <span class="badge {badge}">{status}</span>
        </li>
        """
    content = f"""
    <h1>Поездки</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Каршеринг – поездки", content))


def trip_detail(request, trip_id):
    """Страница /trips/<id>/: карточка поездки или 404."""
    users_list = load_users()
    cars_list = load_cars(users_list)
    trip = find_trip_by_id(load_trips(cars_list, users_list), trip_id)
    if trip is None:
        content = """
        <h1 class="text-danger">Поездка не найдена</h1>
        <a href="/trips/" class="btn btn-outline-secondary">
            ← к списку поездок
        </a>
        """
        return HttpResponse(
            page("Поездка не найдена", content),
            status=404,
        )

    status = "отменена" if trip.is_cancelled else "активна"
    badge = "bg-secondary" if trip.is_cancelled else "bg-success"
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Поездка №{trip.id}</h5>
            <p class="card-text">
                Автомобиль:
                <a href="/cars/{trip.car.id}/">
                    {escape(trip.car.full_name)}
                    ({escape(trip.car.number)})
                </a>
            </p>
            <p class="card-text">
                Владелец: {escape(trip.car.owner.name)}
            </p>
            <p class="card-text">
                Арендатор: {escape(trip.user.name)}
            </p>
            <p class="card-text">
                Дата: {format_date(trip.trip_date)}
            </p>
            <p class="card-text">
                Длительность: {trip.hours} ч.
            </p>
            <p class="card-text">Стоимость: {trip.price} руб.</p>
            <p class="card-text">
                Статус: <span class="badge {badge}">{status}</span>
            </p>
            <a href="/trips/" class="btn btn-outline-secondary">
                ← к списку поездок
            </a>
        </div>
    </div>
    """
    return HttpResponse(
        page(f"Поездка №{trip.id}", content),
        status=200,
    )
