"""
Serializers for drone APIs
"""
import logging

from core.models import Drone, Medication

from rest_framework.exceptions import ParseError
from rest_framework import serializers

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


class DroneManageSerializer(DroneSerializer):
    """Serializer for drone detail view."""
    medications = MedicationSerializer(many=True, read_only=True)
    drone_model = ChoicesField(Drone.DRONE_MODEL, read_only=True)
    state = ChoicesField(Drone.DRONE_STATUS, read_only=False)

    class Meta(DroneSerializer.Meta):
        fields = DroneSerializer.Meta.fields + [
            'medications',
            ]
        read_only_fields = [
            'weight_limit',
            'medications',
            'serial_number',
        ]

    def update(self, instance, validated_data):
        """Manage drone instance battery and state."""

        state = validated_data.pop('state', None)
        battery = validated_data.pop('battery', None)

        if len(validated_data) > 0:
            raise ParseError(detail='You cannot modify the following fields:'
                                    f' {[vl for vl in validated_data]}.')

        if state is not None:
            if state == Drone.DRONE_STATUS.ldg:
                if battery is not None:
                    if battery < 25:
                        raise ParseError(detail='You cannot set the state to'
                                                ' loading if the battery is '
                                                'below 25%.')
            elif state == Drone.DRONE_STATUS.dld:
                instance.weight_limit = None
                instance.medications.clear()

            instance.state = state

        if battery is not None:
            if instance.battery != battery:
                logging.getLogger('battery_log').info(
                    f'[{instance.serial_number}] Battery Change -> '
                    f'from:{instance.battery}% -> to:{battery}%'
                    )
            instance.battery = battery

        instance.save()
        return instance


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
        medications = validated_data.pop('medications', None)

        if len(validated_data) > 0:
            raise ParseError(detail='You cannot modify the following fields:'
                                    f' {[vl for vl in validated_data]}.')

        if instance.state == Drone.DRONE_STATUS.ldg:
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
                                    'Loading state.')

        instance.save()
        return instance
