from django.conf import settings
from django.urls.conf import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from ado.apps.buses.api.views import BusesViewSet, PassengerView
from ado.apps.drivers.api.views import DriverViewSet
from ado.apps.passengers.api.views import PassengerViewSet
from ado.apps.routes.api.views import RouteViewSet
from ado.apps.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("passenger", PassengerViewSet, basename="passengers")
router.register("drivers", DriverViewSet, basename="drivers")
router.register("buses", BusesViewSet, basename="buses")
router.register("route", RouteViewSet, basename="route")

urlpatterns = [
    path('add/passenger/<int:pk>/', PassengerView.as_view(), name="add_passenger")
]

app_name = "api"
urlpatterns += router.urls
