"""
Serializers for drone APIs
"""
from rest_framework import serializers

from core.models import Drone
from medication.serializers import MedicationSerializer


class DroneSerializer(serializers.ModelSerializer):
    """Serializer for drones."""
    medications = MedicationSerializer(many=True, required=False)

    class Meta:
        model = Drone
        lookup_field = 'serial_number'
        fields = [
            'serial_number',
            'battery',
            'state',
            'medications'
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
