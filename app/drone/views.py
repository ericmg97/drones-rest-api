"""
Views for the drone API.
"""
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.db.models import Q
from core.models import Drone
from drone import serializers


class DroneViewSet(viewsets.ModelViewSet):
    """View for manage drone APIs."""

    serializer_class = serializers.DroneDetailSerializer
    queryset = Drone.objects.all()
    http_method_names = ['get', 'post', 'delete']
    lookup_field = 'serial_number'
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve drones for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by(
            'serial_number'
        )

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.DroneSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create new drone."""
        serializer.save(user=self.request.user)

    @action(detail=False, serializer_class=serializers.DroneSerializer)
    def check_available(self, *args, **kwargs):
        """List all available drones to load medications."""

        available_drones = Drone.objects.filter(Q(state=0) | Q(state=1))
        serializer = serializers.DroneSerializer(available_drones, many=True)

        return Response(serializer.data)

    @action(detail=True,
            serializer_class=serializers.DroneAddSerializer,
            methods=['post'])
    def load_medication(self, request, *args, **kwargs):
        """Loads the medication into the selected drone."""
        obj = self.get_object()

        serializer = serializers.DroneAddSerializer(
            obj,
            context={'request': request})
        serializer.update(obj, request.data)

        return Response(serializer.data)

    @action(detail=True,
            serializer_class=serializers.DroneMedsSerializer)
    def check_medication(self, request, *args, **kwargs):
        """Return the medications loaded into the selected drone."""
        obj = self.get_object()

        serializer = serializers.DroneMedsSerializer(
            obj,
            context={'request': request})

        return Response(serializer.data)

    @action(detail=True, serializer_class=serializers.DroneBatterySerializer)
    def check_battery(self, request, *args, **kwargs):
        """Check the battery of the drone."""
        obj = self.get_object()

        serializer = serializers.DroneBatterySerializer(
            obj,
            context={'request': request})

        return Response(serializer.data)
