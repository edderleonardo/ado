from django.db.models import Count
from django_filters import rest_framework as filters
from rest_framework import generics, serializers, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from ado.apps.buses.api.serializers import BusSerializer, SeatSerializerHelper
from ado.apps.buses.models import Bus, Seat
from ado.apps.passengers.models import Passenger


class BusesFilter(filters.FilterSet):
    num_pass = filters.NumberFilter(method='filter_num_pass')

    class Meta:
        model = Bus
        fields = ['route', 'num_pass']

    def filter_num_pass(self, queryset, name, value):
        return queryset.filter(num_pass=value)


class BusesViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.all().order_by('pk').annotate(num_pass=Count('seats__passenger') * 100 / 10)
    serializer_class = BusSerializer
    filterset_class = BusesFilter


class PassengerView(generics.UpdateAPIView):
    queryset = Seat.objects.all().order_by('seat_number')
    serializer_class = SeatSerializerHelper
    lookup_field = 'pk'

    # def _get_create_passenger(self, name):
    #     return Passenger.objects.get_or_create(name=name)

    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     user, _ = self._get_create_passenger(request.data.get('user'))
    #     instance.passenger = user
    #     instance.save()
    #     print("=> ", instance)
    #     print(instance.passenger)
    #     return instance
