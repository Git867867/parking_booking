"""Views for homepage and common page helpers."""

from html import escape

from django.http import HttpRequest, HttpResponse


def page(title: str, content: str) -> str:
    """Вернуть общий HTML-каркас страницы."""
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<link rel="stylesheet" href="{bootstrap}">
</head>
<body class="bg-light">
<nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
<div class="container">
<a class="navbar-brand" href="/">Parking</a>
<div class="navbar-nav">
<a class="nav-link" href="/">Главная</a>
<a class="nav-link" href="/spots/">Места</a>
<a class="nav-link" href="/bookings/">Бронирования</a>
</div>
</div>
</nav>
<main class="container">{content}</main>
</body>
</html>"""


def index(request: HttpRequest) -> HttpResponse:
    """Вернуть главную страницу."""
    content = """
<h1 class="display-5">Система бронирования парковочных мест</h1>
<p class="lead">Веб-интерфейс для просмотра мест и бронирований.</p>
<p>Основные разделы:</p>
<a href="/spots/" class="btn btn-primary me-2">Парковочные места</a>
<a href="/bookings/" class="btn btn-secondary">Бронирования</a>
"""
    return HttpResponse(page("Парковка", content))


def page_not_found(
    request: HttpRequest,
    exception: Exception,
) -> HttpResponse:
    """Вернуть пользовательскую страницу ошибки 404."""
    content = """
<h1 class="text-danger">404 – страница не найдена</h1>
<p>Проверьте адрес или вернитесь на главную.</p>
<a href="/" class="btn btn-primary">На главную</a>
"""
    return HttpResponse(page("404 – страница не найдена", content), status=404)
