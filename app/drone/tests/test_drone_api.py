"""
Tests for drone APIs.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Drone, Medication

from drone.serializers import (
    DroneSerializer,
    DroneDetailSerializer,
    )


DRONES_URL = reverse('drone:drone-list')


def detail_url(drone_sn):
    """Create and return a drone detail URL."""
    return reverse('drone:drone-detail', args=[drone_sn])


def add_med_url(drone_sn):
    """Create and return a drone load-medication URL."""
    return reverse('drone:drone-load-medication', args=[drone_sn])


def create_drone(user, serial_number, **params):
    """Create and return a sample drone."""
    drone = Drone.objects.create(
        user=user,
        serial_number=serial_number,
        **params
    )
    return drone


def create_medication(user, code, name='Testing', weight='200'):
    """Create and return a new medication."""
    return Medication.objects.create(
        user=user,
        code=code,
        name=name,
        weight=weight
    )


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
        }
        res = self.client.post(DRONES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        drone = Drone.objects.get(serial_number=res.data['serial_number'])
        for k, v in payload.items():
            self.assertEqual(getattr(drone, k), v)
        self.assertEqual(drone.user, self.user)

    def test_cannot_update(self):
        """Test that put and patch enpoints are disabled."""
        drone = create_drone(user=self.user, serial_number='Test1')
        url = detail_url(drone.serial_number)

        payload = {'serial_number': 'test23'}
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

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
        """Test trying to delete another users drone gives error."""

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

    def test_add_medication_drone(self):
        """Test add a medication to selected drone."""
        drone = create_drone(
            user=self.user,
            serial_number='Test1',
            drone_model=3)

        medication = create_medication(user=self.user, code='TEST1')
        medication2 = create_medication(user=self.user, code='TEST2')

        payload = {'medications': ['TEST1', 'TEST2']}
        url = add_med_url(drone.serial_number)
        res = self.client.post(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(medication2, drone.medications.all())
        self.assertIn(medication, drone.medications.all())

    def test_add_duplicate_medications_drone(self):
        """Test error when trying to add the same medication."""
        drone = create_drone(user=self.user, serial_number='Test1')
        medication = create_medication(user=self.user, code='TEST1')

        payload = {'medications': ['TEST1', 'TEST1']}
        url = add_med_url(drone.serial_number)
        res = self.client.post(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn(medication, drone.medications.all())

    def test_add_medication_overweight_drone(self):
        """Test add a medication overweight to selected drone."""
        drone = create_drone(
            user=self.user,
            serial_number='Test1'
            )

        medication = create_medication(
            user=self.user,
            code='TEST1',
            weight=400
            )

        medication2 = create_medication(
            user=self.user,
            code='TEST2'
            )

        payload = {'medications': ['TEST1', 'TEST2']}
        url = add_med_url(drone.serial_number)
        res = self.client.post(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn(medication2, drone.medications.all())
        self.assertNotIn(medication, drone.medications.all())

    def test_add_medications_cannot_load_drone(self):
        """Test add medications to overweight the selected drone."""
        drone = create_drone(
            user=self.user,
            serial_number='Test1',
            drone_model=3,
            )

        medication = create_medication(
            user=self.user,
            code='TEST1',
            weight=301
            )

        url = add_med_url(drone.serial_number)

        payload = {'medications': ['TEST1']}
        res1 = self.client.post(url, payload, format='json')

        self.assertEqual(res1.status_code, status.HTTP_200_OK)

        medication2 = create_medication(user=self.user, code='TEST2')

        payload = {'medications': ['TEST2']}
        res = self.client.post(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn(medication2, drone.medications.all())
        self.assertIn(medication, drone.medications.all())

    def test_add_medication_moving_drone(self):
        """Test add a medication to a drone that is moving."""
        drone = create_drone(
            user=self.user,
            serial_number='Test1',
            state=Drone.DRONE_STATUS.ret,
            )

        medication = create_medication(
            user=self.user,
            code='TEST1',
            weight=100
            )

        payload = {'medications': ['TEST1']}
        url = add_med_url(drone.serial_number)
        res = self.client.post(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn(medication, drone.medications.all())

    def test_drone_list_medication(self):
        """Test list all medications that are loaded into a drone."""
        drone = create_drone(
            user=self.user,
            serial_number='Test1',
            state=Drone.DRONE_STATUS.idl,
            )

        medication = create_medication(
            user=self.user,
            code='TEST1',
            weight=100
            )

        self.client.post(
            add_med_url(drone.serial_number),
            {'medications': ['TEST1']},
            format='json')

        url = reverse(
            'drone:drone-check-medication',
            args=[drone.serial_number]
            )

        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for k, v in res.data['medications'][0].items():
            self.assertEqual(getattr(medication, k), v)
