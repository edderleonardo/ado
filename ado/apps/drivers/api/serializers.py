from rest_framework import serializers

from ado.apps.drivers.models import Driver


class DriverSerializer(serializers.ModelSerializer):

    class Meta:
        model = Driver
        fields = [
            'pk',
            'name'
        ]
