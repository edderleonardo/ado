from django.test import TestCase
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APIClient

from ado.apps.passengers.models import Passenger
from ado.utils.testing import create_and_login_user

fake = Faker()

PASSENGER_URL_CREATE_LIST = reverse('api:passengers-list')


class PublicPassengerTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_get_passengers(self):
        """try to get passengers unauthenticated"""
        res = self.client.get(PASSENGER_URL_CREATE_LIST)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(res.status_code, status.HTTP_200_OK)


class PrivatePassengerTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        create_and_login_user(self.client)
        self.fake_passenger_name = "{0} {1}".format(fake.first_name(), fake.last_name())

    def test_get_passengers(self):
        """Try to get passengers objects authenticated"""
        res = self.client.get(PASSENGER_URL_CREATE_LIST)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_passenger(self):
        """create passenger"""
        payload = {
            "name": self.fake_passenger_name
        }

        res = self.client.post(PASSENGER_URL_CREATE_LIST, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['name'], self.fake_passenger_name)

    def test_update_passenger(self):
        """Update passenger"""
        passenger = Passenger.objects.create(name=self.fake_passenger_name)
        update_passenger_name = "{0} {1}".format(fake.first_name(), fake.last_name())

        payload = {
            "name": update_passenger_name
        }

        res = self.client.put(reverse('api:passengers-detail', kwargs={'pk': passenger.id}), payload)

        new_passenger_name = Passenger.objects.get(pk=passenger.id)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(new_passenger_name.name, update_passenger_name)
        self.assertNotEqual(update_passenger_name, self.fake_passenger_name)

    def test_delete_passeger(self):
        passenger = Passenger.objects.create(name=self.fake_passenger_name)

        res = self.client.delete(reverse('api:passengers-detail', kwargs={'pk': passenger.id}))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
