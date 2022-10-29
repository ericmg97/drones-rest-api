"""
Views for the medications API.
"""
from rest_framework.exceptions import PermissionDenied
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Medication, Drone
from medication import serializers


class MedicationViewSet(viewsets.ModelViewSet):
    """View for manage medications APIs."""
    serializer_class = serializers.MedicationSerializer
    queryset = Medication.objects.all()
    http_method_names = ['get', 'post', 'delete']
    lookup_field = 'code'
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_destroy(self, medication):
        """Destroy the medication."""
        if Drone.objects.filter(medications__code=medication.code).exists():
            raise PermissionDenied(
                detail='The medication is currently inside of a dron.'
            )

        return Medication.delete(medication)

    def perform_create(self, serializer):
        """Create new medication."""
        serializer.save(user=self.request.user)
