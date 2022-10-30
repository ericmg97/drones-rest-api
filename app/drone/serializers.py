"""
Serializers for drone APIs
"""
from rest_framework import serializers

from core.models import Drone
from medication.serializers import MedicationSerializer


class ChoicesField(serializers.ChoiceField):
    """Custom ChoiceField serializer field."""

    def __init__(self, choices, **kwargs):
        """init."""
        self._choices = choices
        super(ChoicesField, self).__init__(choices, **kwargs)

    def to_representation(self, obj):
        """Used while retrieving value for the field."""
        return self._choices[obj]

    def to_internal_value(self, data):
        """Used while storing value for the field."""
        for i in range(len(self._choices)):
            try:
                if i == int(data):
                    return i
            except:
                if str(self._choices[i]) == data:
                    return i
            
        raise serializers.ValidationError(f"Acceptable values are {dict(self._choices)}.")


class DroneSerializer(serializers.ModelSerializer):
    """Serializer for drones."""
    drone_model = ChoicesField(Drone.DRONE_MODEL)
    state = serializers.CharField(source='get_state_display', read_only=True)

    class Meta:
        model = Drone
        lookup_field = 'serial_number'
        fields = [
            'serial_number',
            'drone_model',
            'battery',
            'state',
            'weight_limit',
            'medications'
            ]
        read_only_fields = [
            'battery',
            'state',
            'medications'
            ]


class DroneDetailSerializer(DroneSerializer):
    """Serializer for drone detail view."""
    medications = MedicationSerializer(many=True, read_only=True)

    class Meta(DroneSerializer.Meta):
        fields = DroneSerializer.Meta.fields + [
            'medications',
            ]
        

class DroneAddSerializer(serializers.ModelSerializer):
    """Serializer for add medication to drone."""
    class Meta:
        model = Drone
        lockup_field = 'serial_number'
        fields = [
            'serial_number',
            'medications',
            ]
        read_only_fields = [
            'serial_number',
            ]