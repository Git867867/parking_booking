"""Views for homepage and common 404 page."""
from django.shortcuts import render


def index(request):
    """Вернуть главную страницу."""
    return render(request, "homepage/index.html")


def page_not_found(request, exception):
    """Вернуть пользовательскую страницу ошибки 404."""
    return render(
        request,
        "homepage/not_found.html",
        status=404,
    )
