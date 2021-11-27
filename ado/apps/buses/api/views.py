from django.db.models import Count
from django_filters import rest_framework as filters
from rest_framework import viewsets

from ado.apps.buses.api.serializers import BusSerializer
from ado.apps.buses.models import Bus


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
