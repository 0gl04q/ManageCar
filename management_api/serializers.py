from rest_framework import serializers
from manual.models import Car


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'car_model',
            'owner',
            'mileage',
            'year',
            'active'
        )
        model = Car
