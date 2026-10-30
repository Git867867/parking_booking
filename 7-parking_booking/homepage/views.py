from django.shortcuts import render


def index(request):
    return render(request, "homepage/index.html")


def page_not_found(request, exception):
    return render(request, "homepage/not_found.html", status=404)
