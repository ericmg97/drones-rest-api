"""
Serializers for drone APIs
"""
from rest_framework import serializers

from core.models import Drone


class DroneSerializer(serializers.ModelSerializer):
    """Serializer for drones."""

    class Meta:
        model = Drone
        lookup_field = 'serial_number'
        fields = [
            'serial_number',
            'battery',
            'state',
            ]
        read_only_fields = [
            'battery',
            'state',
            ]


class DroneDetailSerializer(DroneSerializer):
    """Serializer for drone detail view."""

    class Meta(DroneSerializer.Meta):
        fields = DroneSerializer.Meta.fields + [
            'drone_model',
            'weight_limit',
            ]
