from django.test import TestCase
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APIClient

from ado.apps.drivers.models import Driver
from ado.utils.testing import create_and_login_user

fake = Faker()

DRIVER_URL_CREATE_LIST = reverse('api:drivers-list')


class PublicDriverTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_get_drivers(self):
        """Try to get drivers objects unauthenticated"""
        res = self.client.get(DRIVER_URL_CREATE_LIST)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(res.status_code, status.HTTP_200_OK)


class PrivateDriveTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        create_and_login_user(self.client)
        self.fake_driver_name = "{0} {1}".format(fake.first_name(), fake.last_name())

    def test_get_drivers(self):
        """Try to get dirvers objects authenticated"""
        res = self.client.get(DRIVER_URL_CREATE_LIST)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_driver(self):
        """Create Driver"""
        payload = {
            'name': self.fake_driver_name
        }

        res = self.client.post(DRIVER_URL_CREATE_LIST, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], self.fake_driver_name)

    def test_update_driver(self):
        """Update driver"""
        driver = Driver.objects.create(name=self.fake_driver_name)
        update_driver_name = "{0} {1}".format(fake.first_name(), fake.last_name())

        payload = {
            'name': update_driver_name
        }

        res = self.client.put(reverse('api:drivers-detail', kwargs={'pk': driver.id}), payload)

        new_driver_name = Driver.objects.get(pk=driver.pk)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(new_driver_name.name, self.fake_driver_name)
        self.assertEqual(new_driver_name.name, update_driver_name)

    def test_list_drivers(self):
        """List drivers"""
        for _ in range(10):
            Driver.objects.create(name='{0} {1}'.format(fake.first_name(), fake.last_name()))

        res = self.client.get(DRIVER_URL_CREATE_LIST)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_driver(self):
        """Delete driver"""
        driver = Driver.objects.create(name=self.fake_driver_name)

        res = self.client.delete(reverse('api:drivers-detail', kwargs={'pk': driver.id}))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
