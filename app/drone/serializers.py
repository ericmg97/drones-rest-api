"""
Serializers for drone APIs
"""
from rest_framework import serializers

from core.models import Drone, Medication


class MedicationSerializer(serializers.ModelSerializer):
    """Serializer for medications."""

    class Meta:
        model = Medication
        fields = [
            'id',
            'code',
            'name',
            'weight'
            ]
        read_only_fields = [
            'id',
        ]


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
