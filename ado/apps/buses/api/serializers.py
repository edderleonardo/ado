from django.db.models import Q
from rest_framework import serializers

from ado.apps.buses.models import Bus, Seat
from ado.apps.drivers.api.serializers import DriverSerializer
from ado.apps.passengers.api.serializers import PassengerSerializer
from ado.apps.passengers.models import Passenger


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
        seats = obj.seats.all().order_by('seat_number')
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
            'pk',
            'seat_number',
            'passenger'
        ]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['passenger'] = PassengerSerializer(instance.passenger).data
        return response


class SeatSerializerHelper(serializers.ModelSerializer):
    passenger = PassengerSerializer(read_only=True)
    user = serializers.CharField(max_length=155, allow_null=False, allow_blank=False, required=True, write_only=True)

    class Meta:
        model = Seat
        fields = [
            'pk',
            'seat_number',
            'user',
            'passenger',
        ]

    def _get_create_passenger(self, name):
        return Passenger.objects.get_or_create(name=name)

    def update(self, instance, validated_data):
        user = validated_data.pop('user')
        instance = super().update(instance, validated_data)
        passenger, _ = self._get_create_passenger(user)
        instance.passenger = passenger
        instance.save()
        return instance
