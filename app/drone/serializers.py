"""
Serializers for drone APIs
"""
from rest_framework import serializers

from core.models import Drone, Medication
from rest_framework.exceptions import ParseError

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
            except ValueError:
                if str(self._choices[i]) == data:
                    return i

        raise serializers.ValidationError(
            f'Acceptable values are {dict(self._choices)}.'
        )


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
            'weight_limit',
            'medications',
            ]


class DroneDetailSerializer(DroneSerializer):
    """Serializer for drone detail view."""
    medications = MedicationSerializer(many=True, read_only=True)

    class Meta(DroneSerializer.Meta):
        fields = DroneSerializer.Meta.fields + [
            'medications',
            ]


class DroneMedsSerializer(serializers.ModelSerializer):
    """Serializer for medications detail view."""
    medications = MedicationSerializer(many=True, read_only=True)

    class Meta():
        model = Drone
        lockup_field = 'serial_number'
        fields = [
            'medications',
            ]
        read_only_fields = [
            'medications',
            ]


class DroneBatterySerializer(serializers.ModelSerializer):
    """Serializer for medications detail view."""

    class Meta():
        model = Drone
        lockup_field = 'serial_number'
        fields = [
            'battery'
            ]
        read_only_fields = [
            'battery',
            ]


class DroneAddSerializer(serializers.ModelSerializer):
    """Serializer for add medication to drone."""
    class Meta:
        model = Drone
        lockup_field = 'serial_number'
        fields = [
            'serial_number',
            'weight_limit',
            'medications',
            ]
        read_only_fields = [
            'weight_limit',
            'serial_number',
            ]

    def update(self, instance, validated_data):
        """Add medication to drone."""
        if instance.state == Drone.DRONE_STATUS.idl or \
                instance.state == Drone.DRONE_STATUS.ldg:

            medications = validated_data.pop('medications', None)

            if len(set(medications)) != len(medications):
                raise ParseError(detail='You cannot load the same '
                                        'medication twice into a drone.')

            if medications is not None and len(medications) > 0:
                insert_meds = []
                auth_user = self.context['request'].user
                user_meds = Medication.objects.filter(user=auth_user)
                drone_remianing_space = instance.weight_limit

                for med in medications:
                    if instance.medications.filter(code=med).exists():
                        raise ParseError(detail=f'The medication {med} '
                                                'is already loaded into this'
                                                ' drone. You cannot load the'
                                                ' same medication twice into'
                                                ' a drone.')

                for med in medications:
                    try:
                        new_med = Medication.objects.get(
                                user=auth_user,
                                code=med
                                )
                        drone_remianing_space -= new_med.weight
                        if drone_remianing_space < 0:
                            raise ParseError(detail='The drone cannot load '
                                                    'the total weight of the'
                                                    ' selected medications.')

                        insert_meds.append(new_med)
                    except Medication.DoesNotExist:
                        if len(user_meds):
                            detail = 'The available medications are '\
                                    f'{[m.code for m in user_meds]}.'
                            raise ParseError(detail=detail)
                        else:
                            raise ParseError(detail='You have to '
                                                    'create a medication '
                                                    'first.')

                for med_get in insert_meds:
                    instance.medications.add(med_get)
                    instance.weight_limit -= med_get.weight
        else:
            raise ParseError(detail='The drone can only be loaded on '
                                    'Idle and Loading states.')

        instance.save()
        return instance
