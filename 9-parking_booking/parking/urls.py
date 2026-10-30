from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("spots/", include("spots.urls")),
    path("bookings/", include("bookings.urls")),
]
