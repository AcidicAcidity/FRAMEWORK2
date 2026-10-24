"""Главная страница и обработчик ошибки 404."""
from django.shortcuts import render


def index(request):
    """Главная страница: описание сервиса и ссылки на разделы."""
    return render(request, "homepage/index.html")


def page_not_found(request, exception):
    """Обработчик handler404: собственная страница для любого 404."""
    return render(request, "404.html", status=404)
