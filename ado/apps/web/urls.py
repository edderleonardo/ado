from django.urls import path

from ado.apps.web.views import (
    BusesView,
    DriversView,
    HomeTemplateView,
    PassengersView,
    RoutesView,
    SalesView,
)

app_name = "web"

urlpatterns = [
    path("", HomeTemplateView.as_view(), name="index"),
    path("pasajeros/", PassengersView.as_view(), name="passengers"),
    path("conductores/", DriversView.as_view(), name="drivers"),
    path("trayectos/", RoutesView.as_view(), name="routes"),
    path("buses/", BusesView.as_view(), name="buses"),
    path("venta/", SalesView.as_view(), name="sales"),
]
