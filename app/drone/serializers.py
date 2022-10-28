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
            'battery',
            'state',
            ]
        read_only_fields = [
            'id',
            'serial_number',
            'battery',
            'state',
            ]


class DroneDetailSerializer(DroneSerializer):
    """Serializer for drone detail view."""

    class Meta(DroneSerializer.Meta):
        fields = DroneSerializer.Meta.fields + [
            'model',
            'weight_limit',
            ]
        read_only_fields = DroneSerializer.Meta.read_only_fields + [
            'model',
            'weight_limit',
            ]
