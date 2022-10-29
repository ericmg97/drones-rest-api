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
            'weight'
            ]
        read_only_fields = [
        ]
