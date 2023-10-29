from rest_framework import serializers
from apps.churchs.models import ChurchDirections


class ChurchDirectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChurchDirections
        fields = (
            "parking",
            "own_car",
            "public_transport",
            "shuttle_bus",
        )
