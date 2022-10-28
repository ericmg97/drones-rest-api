"""
Views for the drone API.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Drone
from drone import serializers


class DroneViewSet(viewsets.ModelViewSet):
    """View for manage drone APIs."""

    serializer_class = serializers.DroneDetailSerializer
    queryset = Drone.objects.all()
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