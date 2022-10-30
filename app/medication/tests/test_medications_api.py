"""
Tests for the medications API.
"""
import tempfile
import os

from PIL import Image

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase


from rest_framework import status
from rest_framework.test import APIClient

from core.models import Medication, Drone

from medication.serializers import MedicationSerializer


MEDICATIONS_URL = reverse('medication:medication-list')


def create_medication(user, code, name='Testing', weight='200'):
    """Create and return a new medication."""
    return Medication.objects.create(
        user=user,
        code=code,
        name=name,
        weight=weight
    )


def image_upload_url(medication_url):
    """Create and return an image upload URL."""
    return reverse('medication:medication-upload-image', args=[medication_url])


def create_drone(user, serial_number, **params):
    """Create and return a sample drone."""
    drone = Drone.objects.create(
        user=user,
        serial_number=serial_number,
        **params
    )
    return drone


def detail_url(medication_code):
    """Create and return a medication detail URL."""
    return reverse('medication:medication-detail', args=[medication_code])


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
    """Test authenticated API requests."""

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

    def test_delete_medication(self):
        """Test deleting a medication."""
        medication = create_medication(self.user, 'TESTING1')

        url = detail_url(medication.code)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        medications = Medication.objects.filter(user=self.user)
        self.assertFalse(medications.exists())

    def test_delete_unused_medication(self):
        """Test deleting a medication cannot be inside of any drone."""
        medication = create_medication(self.user, 'TESTING1')
        drone = create_drone(self.user, 'TESTING')
        drone.medications.add(medication)

        url = detail_url(medication.code)
        self.client.delete(url)

        medications = Medication.objects.filter(user=self.user)
        self.assertTrue(medications.exists())


class ImageUploadTests(TestCase):
    """Tests for the image upload API."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            'user@example.com',
            '12345678'
        )
        self.client.force_authenticate(self.user)
        self.medication = create_medication(user=self.user, code='TEST123')

    def tearDown(self):
        self.medication.image.delete()

    def test_upload_image(self):
        """Test uploading an image to a medication."""
        url = image_upload_url(self.medication.code)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (10, 10))
            img.save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {'image': image_file}
            res = self.client.post(url, payload, format='multipart')

        self.medication.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.medication.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading invalid image."""
        url = image_upload_url(self.medication.code)
        payload = {'image': 'notanimage'}
        res = self.client.post(url, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
