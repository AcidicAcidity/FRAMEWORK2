"""Главная страница, общий HTML-каркас page() и страница ошибки 404."""
from django.http import HttpResponse
from django.utils.html import escape

BOOTSTRAP_CSS = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
    "/dist/css/bootstrap.min.css"
)


def page(title, content):
    """Собрать HTML-документ: кодировка, Bootstrap, навигация, содержимое.

    title попадает в <title> и экранируется; content — готовая разметка,
    в которую view-функции подставляют уже экранированные данные.
    """
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(title)}</title>
    <link rel="stylesheet" href="{BOOTSTRAP_CSS}">
</head>
<body>
    <nav class="nav">
        <a class="nav-link" href="/">Главная</a>
        <a class="nav-link" href="/cars/">Автомобили</a>
        <a class="nav-link" href="/trips/">Поездки</a>
    </nav>
    <main class="container">{content}</main>
</body>
</html>"""


def index(request):
    """Главная страница: описание сервиса и кнопки-ссылки на разделы."""
    content = """
    <h1 class="display-4">Каршеринг</h1>
    <p class="lead">Система совместного использования автомобилей.</p>
    <p>Основные разделы:</p>
    <a href="/cars/" class="btn btn-primary me-2">Автомобили</a>
    <a href="/trips/" class="btn btn-secondary">Поездки</a>
    """
    return HttpResponse(page("Каршеринг", content))


def page_not_found(request, exception):
    """Обработчик handler404: собственная страница для любого 404."""
    content = """
    <h1 class="text-danger">404 – страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 – страница не найдена", content),
        status=404,
    )
