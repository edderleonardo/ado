import datetime

import pytest
from django.contrib.auth import get_user_model
from faker import Faker

from ado.apps.buses.models import Bus, Seat
from ado.apps.drivers.models import Driver
from ado.apps.passengers.models import Passenger
from ado.apps.routes.models import Route

pytestmark = pytest.mark.django_db
fake = Faker()
User = get_user_model()


def create_and_login_user(client, admin=None):
    username = fake.free_email()
    password = fake.password(length=12)

    user = User.objects.create_user(username=username, email=username)
    if admin:
        user.is_staff = True
    user.set_password(password)
    user.save()
    client.login(username=username, password=password)

    return user


def create_driver(name=fake.first_name()):
    return Driver.objects.create(name=name)


def create_bus(code=fake.license_plate(), description=fake.color_name()):
    driver = Driver.objects.create(name=fake.first_name())
    return Bus.objects.create(code=code, description=description, driver=driver)


def create_passenger():
    return Passenger.objects.create(name=fake.first_name())


def create_fake_data_buses_routes():
    bus = create_bus()
    bus_2 = create_bus(code="34X2")

    route = Route.objects.create(name="Route 1", schedule=datetime.datetime.now(tz=datetime.timezone.utc))
    route.buses.add(bus)
    route.buses.add(bus_2)
    route.save()

    other_bus = create_bus(code="OtherBus")
    route_two = Route.objects.create(name="Route 2", schedule=datetime.datetime.now(tz=datetime.timezone.utc))
    route_two.buses.add(other_bus)
    route_two.save()

    p1 = create_passenger()
    p2 = create_passenger()
    p3 = create_passenger()
    p4 = create_passenger()
    # add passengers
    seat = Seat.objects.get(bus=bus, seat_number=1)
    seat.passenger = p1
    seat.save()
    seat = Seat.objects.get(bus=bus, seat_number=2)
    seat.passenger = p2
    seat.save()
    seat = Seat.objects.get(bus=bus, seat_number=3)
    seat.passenger = p3
    seat.save()
    seat = Seat.objects.get(bus=bus, seat_number=4)
    seat.passenger = p4
    seat.save()
