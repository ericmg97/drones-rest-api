"""
Tests for the medications API.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase


from rest_framework import status
from rest_framework.test import APIClient

from core.models import Medication

from drone.serializers import MedicationSerializer


MEDICATIONS_URL = reverse('medication:medication-list')


def create_medication(user, code, name='Testing', weight='200'):
    """Create and return a new medication."""
    return Medication.objects.create(
        user=user,
        code=code,
        name=name,
        weight=weight
    )


def detail_url(medication_id):
    """Create and return a medication detail URL."""
    return reverse('drone:medication-detail', args=[medication_id])


def create_user(email='user@example.com', password='12345678'):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email=email, password=password)


class PublicMedicationsApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving medications."""
        res = self.client.get(MEDICATIONS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateMedicationsApiTests(TestCase):
    """Tesst authenticated API requests."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_medications(self):
        """Test retrieving a list of medications."""
        create_medication(user=self.user, code='TESTING1')
        create_medication(user=self.user, code='TESTING2')

        res = self.client.get(MEDICATIONS_URL)

        medications = Medication.objects.all().order_by('-name')
        serializer = MedicationSerializer(medications, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_medications_limited_to_user(self):
        """Test list of medications is limited to authenticated user."""
        user2 = create_user(email='user2@example.com')
        create_medication(user=user2, code='TESTING1')
        medication = create_medication(user=self.user, code='TESTING2')

        res = self.client.get(MEDICATIONS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['code'], medication.code)
        self.assertEqual(res.data[0]['name'], medication.name)
