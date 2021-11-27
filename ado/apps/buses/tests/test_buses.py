import datetime

from django.conf import settings
from django.test.testcases import TestCase
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APIClient

from ado.apps.buses.models import Bus, Seat
from ado.apps.routes.models import Route
from ado.utils.testing import (
    create_and_login_user,
    create_bus,
    create_driver,
    create_fake_data_buses_routes,
    create_passenger,
)

fake = Faker()

BUS_URL_CREATE_LIST = reverse('api:buses-list')


class PublicBusesTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_get_buses(self):
        """ Try to get buses objects unauthenticated"""
        res = self.client.get(BUS_URL_CREATE_LIST)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(res.status_code, status.HTTP_200_OK)


class PrivateBusesTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        create_and_login_user(self.client)
        self.fake_bus_code = fake.license_plate()
        self.fake_bus_description = fake.color_name()
        self.fake_driver = create_driver()

    def test_get_buses(self):
        """ Try to get buses objects unauthenticated"""
        res = self.client.get(BUS_URL_CREATE_LIST)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_bus(self):
        """create bus"""
        payload = {
            "code": self.fake_bus_code,
            "description": self.fake_bus_description,
            "driver": self.fake_driver.pk
        }

        res = self.client.post(BUS_URL_CREATE_LIST, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_bus_seats(self):
        """create bus"""
        payload = {
            "code": self.fake_bus_code,
            "description": self.fake_bus_description,
            "driver": self.fake_driver.pk
        }

        res = self.client.post(BUS_URL_CREATE_LIST, payload)

        seats = Seat.objects.filter(bus__code=res.data['code']).count()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(seats, settings.SEAT_BY_BUS)

    def test_update_bus(self):
        """Update Bus"""
        bus = Bus.objects.create(code=self.fake_bus_code,
                                 description=self.fake_bus_description, driver=self.fake_driver)
        new_bus_code = fake.license_plate()
        new_bus_description = fake.color_name()
        new_bus_driver = create_driver()

        payload = {
            "code": new_bus_code,
            "description": new_bus_description,
            "driver": new_bus_driver.pk
        }

        res = self.client.put(reverse('api:buses-detail', kwargs={'pk': bus.id}), payload)

        bus_updated = Bus.objects.get(pk=bus.id)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(bus_updated.code, self.fake_bus_code)
        self.assertNotEqual(bus_updated.description, self.fake_bus_description)
        self.assertEqual(bus_updated.code, new_bus_code)
        self.assertEqual(bus_updated.description, new_bus_description)
        self.assertNotEqual(bus_updated.driver, self.fake_driver)
        self.assertEqual(bus_updated.driver, new_bus_driver)

    def test_list_buses(self):
        """List all buses"""
        for _ in range(10):
            Bus.objects.create(code=self.fake_bus_code, description=self.fake_bus_description, driver=create_driver())

        res = self.client.get(BUS_URL_CREATE_LIST)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['count'], 10)

    def test_delete_bus(self):
        bus = Bus.objects.create(code=self.fake_bus_code,
                                 description=self.fake_bus_description, driver=create_driver())

        res = self.client.delete(reverse('api:buses-detail', kwargs={'pk': bus.id}))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotEqual(res.status_code, status.HTTP_200_OK)

    def test_filter_buses(self):
        """Filter buses by route and avg"""
        create_fake_data_buses_routes()
        route_one = Route.objects.get(name="Route 1")
        route_two = Route.objects.get(name="Route 2")
        # Route with data (40%)
        res = self.client.get('/api/v1/buses/?route={0}&num_pass={1}'.format(route_one.pk, 40))
        # Route without data
        res_two = self.client.get('/api/v1/buses/?route={0}&num_pass={1}'.format(route_two.pk, 40))
        # The route not exist
        res_three = self.client.get('/api/v1/buses/?route=10')

        self.assertEqual(res.data['count'], 1)
        self.assertNotEqual(res.data['count'], 0)
        self.assertEqual(res_two.data['count'], 0)
        self.assertNotEqual(res_two.data['count'], 1)
        self.assertEqual(res_three.status_code, status.HTTP_400_BAD_REQUEST)
