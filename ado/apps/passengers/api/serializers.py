from rest_framework import fields, serializers

from ado.apps.passengers.models import Passenger


class PassengerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Passenger
        fields = [
            "pk",
            "name"
        ]
