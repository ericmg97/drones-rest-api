"""
Views for the drone API.
"""
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Drone, Medication
from drone import serializers


class DroneViewSet(viewsets.ModelViewSet):
    """View for manage drone APIs."""

    serializer_class = serializers.DroneDetailSerializer
    queryset = Drone.objects.all()
    http_method_names = ['get', 'post', 'delete']
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve drones for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.DroneSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create new drone."""
        serializer.save(user=self.request.user)


class MedicationViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """View for manage medications APIs."""
    serializer_class = serializers.MedicationSerializer
    queryset = Medication.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')
