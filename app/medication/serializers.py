"""
Serializers for medication APIs
"""
from rest_framework import serializers

from core.models import Medication


class MedicationSerializer(serializers.ModelSerializer):
    """Serializer for medications."""

    class Meta:
        model = Medication
        lookup_field = 'code'
        fields = [
            'code',
            'name',
            'weight',
            'image'
            ]
        read_only_fields = [
        ]


class MedicationImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to recipe."""

    class Meta:
        model = Medication
        fields = ['code', 'image']
        read_only_fields = ['code']
        extra_kwargs = {'image': {'required': 'True'}}
