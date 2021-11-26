import pytest
from django.contrib.auth import get_user_model
from faker import Faker

from ado.apps.buses.models import Bus
from ado.apps.drivers.models import Driver
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
