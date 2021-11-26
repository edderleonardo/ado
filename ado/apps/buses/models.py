from django.db import models
from ado.apps.passengers.models import Passenger
from ado.apps.drivers.models import Driver


class Bus(models.Model):
    code = models.CharField(max_length=50)
    description = models.TextField()
    driver = models.OneToOneField(Driver, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Bus"
        verbose_name_plural = "Buses"

    def __str__(self) -> str:
        return self.code


class Seat(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.IntegerField()
    passenger = models.ForeignKey(Passenger, on_delete=models.SET_NULL, null=True, related_name="seats_passengers")

    def __str__(self):
        return "Bus: {0} - Asiento {1}".format(self.bus.code, self.seat_number)
