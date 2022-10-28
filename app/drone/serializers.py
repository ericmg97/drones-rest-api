"""
Serializers for drone APIs
"""
from rest_framework import serializers

from core.models import Drone


class DroneSerializer(serializers.ModelSerializer):
    """Serializer for drones."""

    class Meta:
        model = Drone
        fields = [
            'id',
            'serial_number',
            'model',
            'weight_limit',
            'battery',
            'state'
            ]
        read_only_fields = [
            'id',
            'serial_number',
            'model',
            'weight_limit',
            'battery',
            'state'
            ]
