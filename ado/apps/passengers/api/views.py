from rest_framework import viewsets

from ado.apps.passengers.api.serializers import PassengerSerializer
from ado.apps.passengers.models import Passenger


class PassengerViewSet(viewsets.ModelViewSet):
    serializer_class = PassengerSerializer
    queryset = Passenger.objects.all().order_by('pk')
