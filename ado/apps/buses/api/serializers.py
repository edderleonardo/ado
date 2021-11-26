from django.db.models import Q
from rest_framework import serializers

from ado.apps.buses.models import Bus, Seat
from ado.apps.drivers.api.serializers import DriverSerializer
from ado.apps.passengers.api.serializers import PassengerSerializer


class BusSerializer(serializers.ModelSerializer):
    seats = serializers.SerializerMethodField()
    avg_passenger = serializers.SerializerMethodField()

    class Meta:
        model = Bus
        fields = [
            'pk',
            'code',
            'description',
            'driver',
            'avg_passenger',
            'seats'
        ]

    def get_seats(self, obj):
        seats = obj.seats.all()
        return SeatSerializer(seats, many=True).data

    def get_avg_passenger(self, obj):
        passengers = obj.seats.filter(~Q(passenger=None)).count()
        return (passengers * 100) / 10

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['driver'] = DriverSerializer(instance.driver).data
        return response


class SeatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seat
        fields = [
            'seat_number',
            'passenger'
        ]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['passenger'] = PassengerSerializer(instance.passenger).data
        return response
