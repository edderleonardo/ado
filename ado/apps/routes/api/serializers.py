from django.db.models import Q
from rest_framework import serializers

from ado.apps.buses.api.serializers import BusSerializer
from ado.apps.routes.models import Route


class RouteSerializer(serializers.ModelSerializer):
    num_buses = serializers.SerializerMethodField()
    avg_passengers = serializers.SerializerMethodField()

    class Meta:
        model = Route
        fields = [
            'name',
            'num_buses',
            'avg_passengers',
            'schedule',
            'buses',
        ]

    def get_num_buses(self, obj):
        return obj.buses.all().count()

    def get_avg_passengers(self, obj):
        num_pass = 0
        for bus in obj.buses.all():
            num_pass += bus.seats.filter(~Q(passenger=None)).count()
        return num_pass / obj.buses.all().count()

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['buses'] = BusSerializer(instance.buses, many=True).data
        return response
