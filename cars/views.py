"""Страницы автомобилей: данные берутся из классов и JSON-хранилища ПР3."""
from datetime import date

from django.http import HttpResponse
from django.utils.html import escape

from homepage.views import page
from models import Car
from models.cars import find_car_by_id
from models.trips import is_car_available
from storage import load_cars, load_trips, load_users


def cars(request):
    """Страница /cars/: список автомобилей."""
    items = ""
    for car in load_cars(load_users()):
        badge = "bg-success" if car.is_available else "bg-secondary"
        status = "доступен" if car.is_available else "недоступен"
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/cars/{car.id}/">
                {escape(car.full_name)} ({escape(car.number)}) –
                {car.price_per_hour} руб./ч
            </a>
            <span class="badge {badge}">{status}</span>
        </li>
        """
    content = f"""
    <h1>Автомобили</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Каршеринг – автомобили", content))


def car_detail(request, car_id):
    """Страница /cars/<id>/: карточка автомобиля или 404."""
    users_list = load_users()
    cars_list = load_cars(users_list)
    car = find_car_by_id(cars_list, car_id)
    if car is None:
        content = """
        <h1 class="text-danger">Автомобиль не найден</h1>
        <a href="/cars/" class="btn btn-outline-secondary">
            ← к списку автомобилей
        </a>
        """
        return HttpResponse(
            page("Автомобиль не найден", content),
            status=404,
        )

    trips_list = load_trips(cars_list, users_list)
    available = is_car_available(trips_list, car, date.today())
    status = "свободен" if available else "занят"
    badge = "bg-success" if available else "bg-danger"
    prices = ""
    for hours in (1, 6, 24):
        discount = Car.get_discount_percent(hours)
        note = f" (скидка {discount}%)" if discount else ""
        prices += f"""
        <li class="list-group-item">
            {hours} ч. – {car.calculate_price(hours)} руб.{note}
        </li>
        """
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{escape(car.full_name)}</h5>
            <p class="card-text"><strong>ID:</strong> {car.id}</p>
            <p class="card-text">
                <strong>Номер:</strong> {escape(car.number)}
            </p>
            <p class="card-text">
                <strong>Владелец:</strong> {escape(car.owner.name)}
            </p>
            <p class="card-text">
                <strong>Стоимость:</strong> {car.price_per_hour} руб./ч
            </p>
            <ul class="list-group mb-3">{prices}</ul>
            <p class="card-text">
                Доступность на текущую дату:
                <span class="badge {badge}">{status}</span>
            </p>
            <a href="/cars/" class="btn btn-outline-secondary">
                ← к списку автомобилей
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(car.full_name, content), status=200)
