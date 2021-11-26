from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from ado.apps.buses.models import Bus, Seat


@receiver(post_save, sender=Bus)
def create_seats(sender, **kwargs):
    if kwargs.get('created', False):
        bus = kwargs['instance']
        index = 1
        for _ in range(settings.SEAT_BY_BUS):
            Seat.objects.create(bus=bus, seat_number=index)
            index += 1

