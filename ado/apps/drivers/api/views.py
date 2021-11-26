from rest_framework import viewsets

from ado.apps.drivers.api.serializers import DriverSerializer
from ado.apps.drivers.models import Driver


class DriverViewSet(viewsets.ModelViewSet):
    serializer_class = DriverSerializer
    queryset = Driver.objects.all().order_by('pk')
