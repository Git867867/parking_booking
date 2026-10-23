from django.urls import path

from . import views

app_name = "spots"

urlpatterns = [
    path("", views.spot_list, name="list"),
    path("<int:spot_id>/", views.spot_detail, name="detail"),
]
