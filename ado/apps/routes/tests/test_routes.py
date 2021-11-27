import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from faker import Faker
from rest_framework import serializers, status
from rest_framework.test import APIClient

from ado.apps.buses.api.serializers import BusSerializer
from ado.apps.buses.models import Bus, Seat
from ado.apps.routes.api.serializers import RouteSerializer
from ado.apps.routes.models import Route
from ado.utils.testing import (
    create_and_login_user,
    create_bus,
    create_driver,
    create_passenger,
)

fake = Faker()
ROUTES_URL_CREATE_LIST = reverse('api:route-list')


class PublicRouteTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_get_routes(self):
        """Try to get routes unauthenticated"""
        res = self.client.get(ROUTES_URL_CREATE_LIST)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(res.status_code, status.HTTP_200_OK)


class PrivateRouteTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        create_and_login_user(self.client)
        self.route_name = fake.street_address()

    def test_get_routes(self):
        res = self.client.get(ROUTES_URL_CREATE_LIST)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_route(self):
        """Create Route"""
        driver = create_driver()

        bus = create_bus(
            code=fake.license_plate(),
            description=fake.color_name())

        payload = {
            "name": self.route_name,
            "schedule": datetime.datetime.now(tz=timezone.utc),
            "buses": [bus.pk]
        }

        res = self.client.post(ROUTES_URL_CREATE_LIST, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data['name'], self.route_name)

    def test_update_route(self):
        driver = create_driver()
        code = fake.license_plate()
        description = fake.color_name()

        bus = create_bus(
            code=code,
            description=description)

        route = Route.objects.create(name=self.route_name, schedule=datetime.datetime.now(tz=timezone.utc))
        route.buses.add(bus)
        route.save()

        new_code = fake.license_plate()
        payload = {
            "name": new_code
        }

        res = self.client.patch(reverse('api:route-detail', kwargs={'pk': route.id}), payload)

        new_route_name = Route.objects.get(pk=route.pk)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(new_route_name.name, self.route_name)
        self.assertEqual(new_route_name.name, new_code)

    def test_list_routes(self):
        """List routes"""
        for _ in range(10):
            route = Route.objects.create(name=fake.street_address(), schedule=datetime.datetime.now(tz=timezone.utc))
            bus = create_bus()
            route.buses.add(bus)
            route.save()

        res = self.client.get(ROUTES_URL_CREATE_LIST)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['count'], 10)

    def test_delete_routes(self):
        """Delete routes"""
        route = Route.objects.create(name=fake.street_address(), schedule=datetime.datetime.now(tz=timezone.utc))
        bus = create_bus()
        route.buses.add(bus)
        route.save()

        res = self.client.delete(reverse('api:route-detail', kwargs={'pk': route.pk}))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_avg_by_route(self):
        """Test filter buses by route"""
        bus = create_bus()
        bus_2 = create_bus(code="34X2")

        route = Route.objects.create(name="Route 1", schedule=datetime.datetime.now(tz=datetime.timezone.utc))
        route.buses.add(bus)
        route.buses.add(bus_2)
        route.save()

        other_bus = create_bus(code="OtherBus")
        route_two = Route.objects.create(name="Route_2", schedule=datetime.datetime.now(tz=datetime.timezone.utc))
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
        seat = Seat.objects.filter(bus=bus)

        buses = Bus.objects.all()
        serializer = BusSerializer(buses, many=True).data

        self.assertEqual(serializer[0]['avg_passenger'], 40.0)
        self.assertNotEqual(serializer[0]['avg_passenger'], 00.0)
        self.assertEqual(serializer[1]['avg_passenger'], 00.0)
        self.assertNotEqual(serializer[1]['avg_passenger'], 40.0)
