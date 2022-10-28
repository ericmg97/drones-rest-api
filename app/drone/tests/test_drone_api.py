"""
Tests for drone APIs.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Drone

from drone.serializers import DroneSerializer


DRONES_URL = reverse('drone:drone-list')


def create_drone(user, serial_number, **params):
    """Create and return a sample drone."""
    drone = Drone.objects.create(
        user=user,
        serial_number=serial_number,
        **params
    )
    return drone


class PublicDroneAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required t ocall API."""
        res = self.client.get(DRONES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateDroneAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()

        self.user = get_user_model().objects.create_user(
            'test@example.com',
            '12345678'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_drones(self):
        """Test retrieving a list of drones"""

        create_drone(user=self.user, serial_number="test1")
        create_drone(user=self.user, serial_number="test2")

        res = self.client.get(DRONES_URL)

        drones = Drone.objects.all().order_by('-id')
        serializer = DroneSerializer(drones, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_drone_list_limited_to_user(self):
        """Test list of drones is limited to authenticated user."""

        other_user = get_user_model().objects.create_user(
            'test2@example.com',
            '12345678',
        )
        create_drone(user=other_user, serial_number='Test1')
        create_drone(user=self.user, serial_number='Test2')

        res = self.client.get(DRONES_URL)

        drones = Drone.objects.filter(user=self.user)
        serializer = DroneSerializer(drones, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
