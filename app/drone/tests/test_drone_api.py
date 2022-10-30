"""
Tests for drone APIs.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Drone

from drone.serializers import (
    DroneSerializer,
    DroneDetailSerializer,
    )


DRONES_URL = reverse('drone:drone-list')


def detail_url(drone_sn):
    """Create and return a drone detail URL."""
    return reverse('drone:drone-detail', args=[drone_sn])


def create_drone(user, serial_number, **params):
    """Create and return a sample drone."""
    drone = Drone.objects.create(
        user=user,
        serial_number=serial_number,
        **params
    )
    return drone


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicDroneAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(DRONES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateDroneAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='test@example.com', password='12345678')
        self.client.force_authenticate(self.user)

    def test_retrieve_drones(self):
        """Test retrieving a list of drones"""

        create_drone(user=self.user, serial_number="test1")
        create_drone(user=self.user, serial_number="test2")

        res = self.client.get(DRONES_URL)

        drones = Drone.objects.all().order_by('serial_number')
        serializer = DroneSerializer(drones, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_drone_list_limited_to_user(self):
        """Test list of drones is limited to authenticated user."""

        other_user = create_user(
            email='test2@example.com',
            password='12345678'
        )
        create_drone(user=other_user, serial_number='Test1')
        create_drone(user=self.user, serial_number='Test2')

        res = self.client.get(DRONES_URL)

        drones = Drone.objects.filter(user=self.user)
        serializer = DroneSerializer(drones, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_drone_detail(self):
        """Test get drone detail."""
        drone = create_drone(user=self.user, serial_number='Test1')

        url = detail_url(drone.serial_number)
        res = self.client.get(url)

        serializer = DroneDetailSerializer(drone)
        self.assertEqual(res.data, serializer.data)

    def test_create_drone(self):
        """Test creating a drone."""
        payload = {
            'serial_number': 'Test1',
            'drone_model': 2,
            'weight_limit': 459,
        }
        res = self.client.post(DRONES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        drone = Drone.objects.get(serial_number=res.data['serial_number'])
        for k, v in payload.items():
            self.assertEqual(getattr(drone, k), v)
        self.assertEqual(drone.user, self.user)

    def test_cannot_update(self):
        """Test that put enpoint is disabled."""
        drone = create_drone(user=self.user, serial_number='Test1')
        url = detail_url(drone.serial_number)

        payload = {'serial_number': 'test23'}
        
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_cannot_create_incorrect_sn(self):
        """Test cannot create drone with incorrect serial number."""

        payload = {'serial_number': 'tst'}
        res = self.client.post(DRONES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Drone.objects.filter(serial_number='tst').exists())

    def test_delete_drone(self):
        """Test deleting a drone successful."""
        drone = create_drone(user=self.user, serial_number='Test1')

        url = detail_url(drone.serial_number)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Drone.objects.filter(serial_number=drone.serial_number).exists()
        )

    def test_delete_other_user_drone_error(self):
        """Test rying to delete another users drone gives error."""

        other_user = create_user(
            email='test2@example.com',
            password='12345678'
        )
        drone = create_drone(user=other_user, serial_number='Test1')

        url = detail_url(drone.serial_number)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(
            Drone.objects.filter(serial_number=drone.serial_number).exists()
        )
